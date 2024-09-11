from django.test import TestCase
from .models import Note


class LogicTestCase(TestCase):
    def test_create_note_authenticated(self):
        user = self.create_user()
        self.client.force_login(user)
        response = self.client.post(reverse('notes:add'), {
                                    'title': 'Test note', 'text': 'Test text'})
        self.assertEqual(response.status_code, 302)

    def test_create_note_anonymous(self):
        response = self.client.post(reverse('notes:add'), {
                                    'title': 'Test note', 'text': 'Test text'})
        self.assertEqual(response.status_code, 302)

    def test_create_note_with_same_slug(self):
        user = self.create_user()
        note1 = self.create_note(user, slug='test-slug')
        response = self.client.post
