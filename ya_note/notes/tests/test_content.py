from notes.forms import NoteForm
from notes.tests.conftest import BaseTestCase


class ContentTests(BaseTestCase):
    """Тесты, наследующиеся от базового тестового класса."""

    def test_note_in_context_of_notes_list(self):
        response = self.client_testuser.get(self.notes_list_url)
        self.assertIn(self.note, response.context['object_list'])

    def test_other_user_note_not_in_notes_list(self):
        response = self.client_otheruser.get(self.notes_list_url)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_form_in_context_of_note_create(self):
        response = self.client_testuser.get(self.add_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_form_in_context_of_note_edit(self):
        response = self.client_testuser.get(self.edit_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
