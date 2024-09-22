import pytest
from http import HTTPStatus

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, status',
    (
        ('news_detail', pytest.lazy_fixture('client'), HTTPStatus.OK),
        ('users_login', pytest.lazy_fixture('client'), HTTPStatus.OK),
        ('users_logout', pytest.lazy_fixture('client'), HTTPStatus.OK),
        ('users_signup', pytest.lazy_fixture('client'), HTTPStatus.OK),
        ('news_edit', pytest.lazy_fixture('client'), HTTPStatus.FOUND),
        ('news_edit', pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        ('edit_other', pytest.lazy_fixture(
            'client'), HTTPStatus.FOUND),
        ('delete_other', pytest.lazy_fixture(
            'client'), HTTPStatus.FOUND),
        ('news_delete', pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        ('news_delete', pytest.lazy_fixture('client'), HTTPStatus.FOUND),
    )
)
def test_status_and_redirects(
    urls,
    reverse_url,
    parametrized_client,
    status,
    news
):
    url = urls[reverse_url]
    response = parametrized_client.get(url)
    assert response.status_code == status
