from pytils.translit import slugify

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model

from notes.forms import WARNING
from notes.models import Note

from notes.tests.conftest import Constants

User = get_user_model()


class LogicTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username=Constants.USERNAME_1, password=Constants.PASSWORD_1)
        cls.other_user = User.objects.create_user(
            username=Constants.USERNAME_2, password=Constants.PASSWORD_2)
        cls.note = Note.objects.create(
            title=Constants.TEST_NOTE_TITLE,
            text=Constants.TEST_NOTE_TEXT,
            author=cls.user,
            slug=Constants.TEST_NOTE_SLUG
        )
        cls.add_url = reverse('notes:add')
        cls.edit_url = reverse('notes:edit', kwargs={
                               'slug': Constants.TEST_NOTE_SLUG})
        cls.delete_url = reverse('notes:delete', kwargs={
                                 'slug': Constants.TEST_NOTE_SLUG})

        cls.client_testuser = cls.client_class()
        cls.client_testuser.login(
            username=Constants.USERNAME_1, password=Constants.PASSWORD_1)

        cls.client_otheruser = cls.client_class()
        cls.client_otheruser.login(
            username=Constants.USERNAME_2, password=Constants.PASSWORD_2)

    def test_logged_in_user_can_create_note(self):
        note_count_before = Note.objects.count()
        self.client_testuser.post(self.add_url, {
            'title': Constants.NEW_NOTE_TITLE,
            'text': Constants.NEW_NOTE_TEXT,
            'slug': Constants.NEW_NOTE_SLUG
        })
        note_count_after = Note.objects.count()
        self.assertEqual(note_count_after, note_count_before + 1)

        new_note = Note.objects.latest('id')
        self.assertEqual(new_note.title, Constants.NEW_NOTE_TITLE)
        self.assertEqual(new_note.text, Constants.NEW_NOTE_TEXT)
        self.assertEqual(new_note.author, self.user)

    def test_anonymous_user_cannot_create_note(self):
        note_count_before = Note.objects.count()
        self.client.post(self.add_url, {
            'title': Constants.NEW_NOTE_TITLE,
            'text': Constants.NEW_NOTE_TEXT,
            'slug': Constants.NEW_NOTE_SLUG
        })
        note_count_after = Note.objects.count()
        self.assertEqual(note_count_after, note_count_before)

    def test_cannot_create_note_with_duplicate_slug(self):
        response = self.client_testuser.post(self.add_url, {
            'title': Constants.ANOTHER_NOTE_TITLE,
            'text': Constants.ANOTHER_NOTE_TEXT,
            'slug': Constants.TEST_NOTE_SLUG
        })
        self.assertFormError(
            response, 'form', 'slug', Constants.TEST_NOTE_SLUG + WARNING
        )

    def test_slug_is_generated_if_not_provided(self):
        Note.objects.all().delete()
        self.client_testuser.post(self.add_url, {
            'title': Constants.GENERATED_NOTE_TITLE,
            'text': Constants.GENERATED_NOTE_TEXT
        })
        note = Note.objects.get(
            title=Constants.GENERATED_NOTE_TITLE)
        expected_slug = slugify(note.title)
        self.assertEqual(note.slug, expected_slug)

    def test_user_can_edit_own_note(self):
        self.client_testuser.post(self.edit_url, {
            'title': Constants.EDITED_NOTE_TITLE,
            'text': Constants.EDITED_NOTE_TEXT,
            'slug': Constants.TEST_NOTE_SLUG
        })
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.title, Constants.EDITED_NOTE_TITLE)
        self.assertEqual(updated_note.text, Constants.EDITED_NOTE_TEXT)
        self.assertEqual(updated_note.slug, Constants.TEST_NOTE_SLUG)
        self.assertEqual(updated_note.author, self.user)

    def test_user_cannot_edit_other_user_note(self):
        self.client_otheruser.post(self.edit_url, {
            'title': Constants.HACKED_NOTE_TITLE,
            'text': Constants.HACKED_NOTE_TEXT,
            'slug': Constants.TEST_NOTE_SLUG
        })
        note_before_update = Note.objects.get(
            id=self.note.id)
        self.assertNotEqual(note_before_update.title,
                            Constants.HACKED_NOTE_TITLE)
        self.assertNotEqual(note_before_update.text,
                            Constants.HACKED_NOTE_TEXT)
        self.assertEqual(note_before_update.slug, Constants.TEST_NOTE_SLUG)
        self.assertEqual(note_before_update.author,
                         self.user)

    def test_user_can_delete_own_note(self):
        note_count_before = Note.objects.count()
        self.client_testuser.post(self.delete_url)
        note_count_after = Note.objects.count()
        self.assertEqual(note_count_after, note_count_before - 1)

    def test_user_cannot_delete_other_user_note(self):
        note_count_before = Note.objects.count()
        self.client_otheruser.post(self.delete_url)
        note_count_after = Note.objects.count()
        self.assertEqual(note_count_after, note_count_before)
