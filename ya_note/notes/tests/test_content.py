from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note

User = get_user_model()


class ContentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.other_user = User.objects.create_user(
            username='otheruser', password='testpass2'
        )
        self.note = Note.objects.create(
            title="Test Note",
            text="Test Text",
            author=self.user,
            slug='test-note'
        )

    def test_note_in_context_of_notes_list(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('notes:list'))
        self.assertIn(self.note, response.context['object_list'])

    def test_other_user_note_not_in_notes_list(self):
        self.client.login(username='otheruser', password='testpass2')
        response = self.client.get(reverse('notes:list'))
        self.assertNotIn(self.note, response.context['object_list'])

    def test_form_in_context_of_note_create(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('notes:add'))
        self.assertIn('form', response.context)

    def test_form_in_context_of_note_edit(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(
            reverse('notes:edit', kwargs={'slug': 'test-note'})
        )
        self.assertIn('form', response.context)
