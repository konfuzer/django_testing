import pytest
from http import HTTPStatus

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, status',
    (
        ('news_detail', 'client', HTTPStatus.OK),
        ('users_login', 'client', HTTPStatus.OK),
        ('users_logout', 'client', HTTPStatus.OK),
        ('users_signup', 'client', HTTPStatus.OK),
        ('news_edit', 'client', HTTPStatus.FOUND),
        ('news_delete', 'client', HTTPStatus.FOUND),
    )
)
def test_status_and_redirects(
    urls,
    reverse_url,
    parametrized_client,
    status, client,
    setup_news
):
    url = urls[reverse_url]
    response = client.get(url)
    assert response.status_code == status


def test_comment_edit_delete_accessible_to_author(client, setup_comment):
    response_edit = client.get(setup_comment['edit_url'])
    response_delete = client.get(setup_comment['delete_url'])
    assert response_edit.status_code == HTTPStatus.OK
    assert response_delete.status_code == HTTPStatus.OK


def test_user_cannot_edit_or_delete_other_users_comments(
        client,
        other_user_comment,
        user_factory
):
    another_user = user_factory(username='another_user')
    client.force_login(another_user)
    response_edit = client.get(other_user_comment['edit_url'])
    response_delete = client.get(other_user_comment['delete_url'])
    assert response_edit.status_code == HTTPStatus.NOT_FOUND
    assert response_delete.status_code == HTTPStatus.NOT_FOUND
