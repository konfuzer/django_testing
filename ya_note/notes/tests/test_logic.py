# django_testing/ya_note/notes/tests/test_logic.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note

User = get_user_model()


class LogicTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.other_user = User.objects.create_user(
            username='otheruser', password='testpass2')
        self.note = Note.objects.create(
            title="Test Note", text="Test Text", author=self.user, slug='test-note')

    def test_logged_in_user_can_create_note(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('notes:add'), {
                                    'title': 'New Note', 'text': 'New Text', 'slug': 'new-note'})
        self.assertEqual(Note.objects.count(), 2)

    def test_anonymous_user_cannot_create_note(self):
        response = self.client.post(reverse('notes:add'), {
                                    'title': 'New Note', 'text': 'New Text', 'slug': 'new-note'})
        self.assertEqual(Note.objects.count(), 1)

    def test_cannot_create_note_with_duplicate_slug(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('notes:add'), {
                                    'title': 'Another Note', 'text': 'Another Text', 'slug': 'test-note'})
        self.assertFormError(response, 'form', 'slug',
                             'test-note - такой slug уже существует, придумайте уникальное значение!')

    def test_slug_is_generated_if_not_provided(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('notes:add'), {
                                    'title': 'Generated Slug Note', 'text': 'Text'})
        note = Note.objects.get(title='Generated Slug Note')
        self.assertEqual(note.slug, 'generated-slug-note')

    def test_user_can_edit_own_note(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('notes:edit', kwargs={'slug': 'test-note'}), {
                                    'title': 'Edited Note', 'text': 'Edited Text', 'slug': 'test-note'})
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Edited Note')

    def test_user_cannot_edit_other_user_note(self):
        self.client.login(username='otheruser', password='testpass2')
        response = self.client.post(reverse('notes:edit', kwargs={'slug': 'test-note'}), {
                                    'title': 'Hacked Note', 'text': 'Hacked Text', 'slug': 'test-note'})
        self.note.refresh_from_db()
        self.assertNotEqual(self.note.title, 'Hacked Note')

    def test_user_can_delete_own_note(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('notes:delete', kwargs={'slug': 'test-note'}))
        self.assertEqual(Note.objects.count(), 0)

    def test_user_cannot_delete_other_user_note(self):
        self.client.login(username='otheruser', password='testpass2')
        response = self.client.post(
            reverse('notes:delete', kwargs={'slug': 'test-note'}))
        self.assertEqual(Note.objects.count(), 1)
