from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()


class RouteTests(TestCase):

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
        cls.home_url = reverse('notes:home')
        cls.notes_list_url = reverse('notes:list')
        cls.note_add_url = reverse('notes:add')
        cls.note_detail_url = reverse(
            'notes:detail', kwargs={'slug': 'test-note'})
        cls.note_edit_url = reverse(
            'notes:edit',
            kwargs={'slug': 'test-note'}
        )
        cls.note_delete_url = reverse(
            'notes:delete', kwargs={'slug': 'test-note'})
        cls.login_url = reverse('users:login')

        cls.client_testuser = cls.client_class()
        cls.client_testuser.login(username='testuser', password='testpass')

        cls.client_otheruser = cls.client_class()
        cls.client_otheruser.login(username='otheruser', password='testpass2')

    def test_home_page_accessible_to_anonymous(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_notes_page_redirects_anonymous(self):
        response = self.client.get(self.notes_list_url)
        self.assertRedirects(response, self.login_url
                             + '?next=' + self.notes_list_url)

    def test_notes_page_accessible_to_authenticated(self):
        response = self.client_testuser.get(self.notes_list_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_add_note_redirects_anonymous(self):
        response = self.client.get(self.note_add_url)
        self.assertRedirects(response, self.login_url
                             + '?next=' + self.note_add_url)

    def test_add_note_accessible_to_authenticated(self):
        response = self.client_testuser.get(self.note_add_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_note_detail_accessible_to_author(self):
        response = self.client_testuser.get(self.note_detail_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_note_detail_inaccessible_to_other_user(self):
        response = self.client_otheruser.get(self.note_detail_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_edit_note_inaccessible_to_other_user(self):
        response = self.client_otheruser.get(self.note_edit_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_note_inaccessible_to_other_user(self):
        response = self.client_otheruser.get(self.note_delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
