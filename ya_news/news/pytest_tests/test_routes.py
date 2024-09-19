import pytest

from django.urls import reverse

from http import HTTPStatus

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url_name, expected_status',
    [
        ('news_detail', HTTPStatus.OK),
        ('users_login', HTTPStatus.OK),
        ('users_logout', HTTPStatus.OK),
        ('users_signup', HTTPStatus.OK),
    ]
)
def test_status_codes(
    client,
    urls,
    setup_news,
    url_name,
    expected_status
):
    url = urls[url_name]
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url_name, expected_redirect_url_name',
    [
        ('news_edit', 'users:login'),
        ('news_delete', 'users:login')
    ]
)
def test_redirects(client, urls, url_name, expected_redirect_url_name):
    response = client.get(urls[url_name])
    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse(expected_redirect_url_name))


def test_comment_edit_delete_accessible_to_author(client, setup_comment):
    response_edit = client.get(setup_comment['edit_url'])
    response_delete = client.get(setup_comment['delete_url'])
    assert response_edit.status_code == HTTPStatus.OK
    assert response_delete.status_code == HTTPStatus.OK


def test_user_cannot_edit_or_delete_other_users_comments(
        client,
        other_user_comment
):
    response_edit = client.get(other_user_comment['edit_url'])
    response_delete = client.get(other_user_comment['delete_url'])
    assert response_edit.status_code == HTTPStatus.NOT_FOUND
    assert response_delete.status_code == HTTPStatus.NOT_FOUND
