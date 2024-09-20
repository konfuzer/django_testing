from pytils.translit import slugify

from django.contrib.auth import get_user_model

from notes.models import Note
from notes.tests.conftest import BaseTestCase


User = get_user_model()


class LogicTests(BaseTestCase):

    def test_logged_in_user_can_create_note(self):
        Note.objects.all().delete()

        note_count_before = Note.objects.count()
        self.client_testuser.post(self.add_url, self.new_note_data)
        note_count_after = Note.objects.count()
        self.assertEqual(note_count_after, note_count_before + 1)

        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.new_note_data['title'])
        self.assertEqual(new_note.text, self.new_note_data['text'])
        self.assertEqual(new_note.author, self.user)

    def test_anonymous_user_cannot_create_note(self):
        note_count_before = Note.objects.count()
        self.client.post(self.add_url, self.new_note_data)
        note_count_after = Note.objects.count()
        self.assertEqual(note_count_after, note_count_before)

    def test_cannot_create_note_with_duplicate_slug(self):
        response = self.client_testuser.post(
            self.add_url, self.duplicate_slug_data)
        self.assertFormError(
            response, 'form', 'slug', self.duplicate_slug_error
        )

    def test_slug_is_generated_if_not_provided(self):
        Note.objects.all().delete()
        self.client_testuser.post(self.add_url, self.generated_note_data)
        note = Note.objects.get()
        expected_slug = slugify(note.title)
        self.assertEqual(note.slug, expected_slug)

    def test_user_can_edit_own_note(self):
        self.client_testuser.post(self.edit_url, self.edit_note_data)
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.title, self.edit_note_data['title'])
        self.assertEqual(updated_note.text, self.edit_note_data['text'])
        self.assertEqual(updated_note.slug, self.edit_note_data['slug'])
        self.assertEqual(updated_note.author, self.note.author)

    def test_user_cannot_edit_other_user_note(self):
        self.client_otheruser.post(self.edit_url, self.hacked_note_data)
        note_after_update_attempt = Note.objects.get(id=self.note.id)
        self.assertEqual(note_after_update_attempt.title, self.note.title)
        self.assertEqual(note_after_update_attempt.text, self.note.text)
        self.assertEqual(note_after_update_attempt.slug, self.note.slug)
        self.assertEqual(note_after_update_attempt.author, self.note.author)

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
