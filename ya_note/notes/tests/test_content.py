from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class BaseContentTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        cls.other_user = User.objects.create_user(
            username='otheruser', password='testpass2'
        )
        cls.note = Note.objects.create(
            title="Test Note",
            text="Test Text",
            author=cls.user,
            slug='test-note'
        )

        cls.notes_list_url = reverse('notes:list')
        cls.note_add_url = reverse('notes:add')
        cls.note_edit_url = reverse('notes:edit', kwargs={'slug': 'test-note'})

        cls.client_testuser = cls.client_class()
        cls.client_testuser.login(username='testuser', password='testpass')

        cls.client_otheruser = cls.client_class()
        cls.client_otheruser.login(username='otheruser', password='testpass2')


class ContentTests(BaseContentTests):

    def test_note_in_context_of_notes_list(self):
        response = self.client_testuser.get(self.notes_list_url)
        self.assertIn(self.note, response.context['object_list'])

    def test_other_user_note_not_in_notes_list(self):
        response = self.client_otheruser.get(self.notes_list_url)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_form_in_context_of_note_create(self):
        response = self.client_testuser.get(self.note_add_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_form_in_context_of_note_edit(self):
        response = self.client_testuser.get(self.note_edit_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
