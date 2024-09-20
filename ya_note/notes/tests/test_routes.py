from http import HTTPStatus

from notes.tests.conftest import BaseTestCase


class RouteTests(BaseTestCase):
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
        response = self.client.get(self.add_url)
        self.assertRedirects(response, self.login_url
                             + '?next=' + self.add_url)

    def test_add_note_accessible_to_authenticated(self):
        response = self.client_testuser.get(self.add_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_note_detail_accessible_to_author(self):
        response = self.client_testuser.get(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_note_detail_inaccessible_to_other_user(self):
        response = self.client_otheruser.get(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_edit_note_inaccessible_to_other_user(self):
        response = self.client_otheruser.get(self.edit_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_note_inaccessible_to_other_user(self):
        response = self.client_otheruser.get(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
