from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()

# Константы для повторяющихся значений
USERNAME_1 = 'testuser'
PASSWORD_1 = 'testpass'
USERNAME_2 = 'otheruser'
PASSWORD_2 = 'testpass2'
TEST_NOTE_TITLE = 'Test Note'
TEST_NOTE_TEXT = 'Test Text'
TEST_NOTE_SLUG = 'test-note'
ANOTHER_NOTE_TITLE = 'Another Note'
ANOTHER_NOTE_TEXT = 'Another Text'
NEW_NOTE_TITLE = 'New Note'
NEW_NOTE_TEXT = 'New Text'
NEW_NOTE_SLUG = 'new-note'
GENERATED_NOTE_TITLE = 'Generated Slug Note'
GENERATED_NOTE_TEXT = 'Text'
EDITED_NOTE_TITLE = 'Edited Note'
EDITED_NOTE_TEXT = 'Edited Text'
HACKED_NOTE_TITLE = 'Hacked Note'
HACKED_NOTE_TEXT = 'Hacked Text'


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username=USERNAME_1, password=PASSWORD_1
        )
        cls.other_user = User.objects.create_user(
            username=USERNAME_2, password=PASSWORD_2
        )
        cls.note = Note.objects.create(
            title=TEST_NOTE_TITLE,
            text=TEST_NOTE_TEXT,
            author=cls.user,
            slug=TEST_NOTE_SLUG
        )
        cls.add_url = reverse('notes:add')
        cls.edit_url = reverse('notes:edit', kwargs={'slug': TEST_NOTE_SLUG})
        cls.delete_url = reverse('notes:delete', kwargs={
                                 'slug': TEST_NOTE_SLUG})


class LogicTests(BaseTestCase):

    def test_logged_in_user_can_create_note(self):
        note_count_before = Note.objects.count()
        self.client.login(username=USERNAME_1, password=PASSWORD_1)
        self.client.post(self.add_url, {
            'title': NEW_NOTE_TITLE,
            'text': NEW_NOTE_TEXT,
            'slug': NEW_NOTE_SLUG
        })
        note_count_after = Note.objects.count()
        self.assertEqual(note_count_after, note_count_before + 1)
        new_note = Note.objects.get(slug=NEW_NOTE_SLUG)
        self.assertEqual(new_note.title, NEW_NOTE_TITLE)
        self.assertEqual(new_note.text, NEW_NOTE_TEXT)
        self.assertEqual(new_note.author, self.user)

    def test_anonymous_user_cannot_create_note(self):
        note_count_before = Note.objects.count()
        self.client.post(self.add_url, {
            'title': NEW_NOTE_TITLE,
            'text': NEW_NOTE_TEXT,
            'slug': NEW_NOTE_SLUG
        })
        note_count_after = Note.objects.count()
        self.assertEqual(note_count_after, note_count_before)

    def test_cannot_create_note_with_duplicate_slug(self):
        self.client.login(username=USERNAME_1, password=PASSWORD_1)
        response = self.client.post(self.add_url, {
            'title': ANOTHER_NOTE_TITLE,
            'text': ANOTHER_NOTE_TEXT,
            'slug': TEST_NOTE_SLUG
        })

        self.assertFormError(
            response, 'form', 'slug', TEST_NOTE_SLUG + WARNING
        )

    def test_slug_is_generated_if_not_provided(self):
        Note.objects.all().delete()
        self.client.login(username=USERNAME_1, password=PASSWORD_1)
        self.client.post(self.add_url, {
            'title': GENERATED_NOTE_TITLE, 'text': GENERATED_NOTE_TEXT
        })
        note = Note.objects.get(title=GENERATED_NOTE_TITLE)
        expected_slug = slugify(note.title)
        self.assertEqual(note.slug, expected_slug)

    def test_user_can_edit_own_note(self):
        self.client.login(username=USERNAME_1, password=PASSWORD_1)
        self.client.post(self.edit_url, {
            'title': EDITED_NOTE_TITLE,
            'text': EDITED_NOTE_TEXT,
            'slug': TEST_NOTE_SLUG
        })
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.title, EDITED_NOTE_TITLE)
        self.assertEqual(updated_note.text, EDITED_NOTE_TEXT)
        self.assertEqual(updated_note.slug, TEST_NOTE_SLUG)
        self.assertEqual(updated_note.author, self.user)

    def test_user_cannot_edit_other_user_note(self):
        self.client.login(username=USERNAME_2, password=PASSWORD_2)
        self.client.post(self.edit_url, {
            'title': HACKED_NOTE_TITLE,
            'text': HACKED_NOTE_TEXT,
            'slug': TEST_NOTE_SLUG
        })
        note_before_update = Note.objects.get(id=self.note.id)
        self.assertNotEqual(note_before_update.title, HACKED_NOTE_TITLE)
        self.assertNotEqual(note_before_update.text, HACKED_NOTE_TEXT)
        self.assertEqual(note_before_update.slug, TEST_NOTE_SLUG)
        self.assertEqual(note_before_update.author, self.user)

    def test_user_can_delete_own_note(self):
        self.client.login(username=USERNAME_1, password=PASSWORD_1)
        self.client.post(self.delete_url)
        self.assertEqual(Note.objects.count(), 0)

    def test_user_cannot_delete_other_user_note(self):
        self.client.login(username=USERNAME_2, password=PASSWORD_2)
        self.client.post(self.delete_url)
        self.assertEqual(Note.objects.count(), 1)
