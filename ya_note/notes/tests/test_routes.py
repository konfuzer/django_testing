from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note

User = get_user_model()


class RouteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.other_user = User.objects.create_user(
            username='otheruser', password='testpass2')
        self.note = Note.objects.create(
            title="Test Note", text="Test Text", author=self.user, slug='test-note')

    def test_home_page_accessible_to_anonymous(self):
        response = self.client.get(reverse('notes:home'))
        self.assertEqual(response.status_code, 200)

    def test_notes_page_redirects_anonymous(self):
        response = self.client.get(reverse('notes:list'))
        self.assertRedirects(response, reverse('login') +
                             '?next=' + reverse('notes:list'))

    def test_notes_page_accessible_to_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, 200)

    def test_add_note_redirects_anonymous(self):
        response = self.client.get(reverse('notes:add'))
        self.assertRedirects(response, reverse('login') +
                             '?next=' + reverse('notes:add'))

    def test_add_note_accessible_to_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('notes:add'))
        self.assertEqual(response.status_code, 200)

    def test_note_detail_accessible_to_author(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(
            reverse('notes:detail', kwargs={'slug': 'test-note'}))
        self.assertEqual(response.status_code, 200)

    def test_note_detail_inaccessible_to_other_user(self):
        self.client.login(username='otheruser', password='testpass2')
        response = self.client.get(
            reverse('notes:detail', kwargs={'slug': 'test-note'}))
        self.assertEqual(response.status_code, 404)

    def test_edit_note_inaccessible_to_other_user(self):
        self.client.login(username='otheruser', password='testpass2')
        response = self.client.get(
            reverse('notes:edit', kwargs={'slug': 'test-note'}))
        self.assertEqual(response.status_code, 404)

    def test_delete_note_inaccessible_to_other_user(self):
        self.client.login(username='otheruser', password='testpass2')
        response = self.client.get(
            reverse('notes:delete', kwargs={'slug': 'test-note'}))
        self.assertEqual(response.status_code, 404)
