from django.test import TestCase, Client
from django.urls import reverse


class RoutesTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_anonymous(self):
        response = self.client.get(reverse('notes:home'))
        self.assertEqual(response.status_code, 200)

    def test_notes_list_authenticated(self):
        user = self.create_user()
        self.client.force_login(user)
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, 200)

    def test_add_note_authenticated(self):
        user = self.create_user()
        self.client.force_login(user)
        response = self.client.get(reverse('notes:add'))
        self.assertEqual(response.status_code, 200)

    def test_done_authenticated(self):
        user = self.create_user()
        self.client.force_login(user)
        response = self.client.get(reverse('notes:success'))
        self.assertEqual(response.status_code, 200)

    def test_note_detail_authenticated(self):
        user = self.create_user()
        note = self.create_note(user)
        self.client.force_login(user)
        response = self.client.get(reverse('notes:detail', args=[note.slug]))
        self.assertEqual(response.status_code, 200)

    def test_note_edit_authenticated(self):
        user = self.create_user()
        note = self.create_note(user)
        self.client.force_login(user)
        response = self.client.get(reverse('notes:edit', args=[note.slug]))
        self.assertEqual(response.status_code, 200)

    def test_note_delete_authenticated(self):
        user = self.create_user()
        note = self.create_note(user)
        self.client.force_login(user)
        response = self.client.get(reverse('notes:delete', args=[note.slug]))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_redirects_to_login(self):
        response = self.client.get(reverse('notes:list'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/notes/')

    def create_user(self):
        pass

    def create_note(self, user):
        pass
