import pytest
from django.urls import reverse
from http import HTTPStatus


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url_name, kwargs, expected_status',
    [
        ('news:detail', {'pk': 1}, HTTPStatus.OK),
        ('users:login', None, HTTPStatus.OK),
        ('users:logout', None, HTTPStatus.OK),
        ('users:signup', None, HTTPStatus.OK)
    ]
)
def test_status_codes(
    client,
    news_factory,
    url_name,
    kwargs,
    expected_status
):
    if url_name == 'news:detail':
        news = news_factory()
        kwargs = {'pk': news.pk}
    url = reverse(url_name, kwargs=kwargs)
    response = client.get(url)
    assert response.status_code == expected_status


# Объединяем тесты на редиректы в один
@pytest.mark.parametrize(
    'url_name, kwargs, expected_redirect_url_name',
    [
        ('news:edit', {'pk': 1}, 'users:login'),
        ('news:delete', {'pk': 1}, 'users:login')
    ]
)
def test_redirects(
    client,
    comment_factory,
    news_factory,
    url_name,
    kwargs,
    expected_redirect_url_name
):
    news = news_factory()
    comment = comment_factory(news=news)
    kwargs = {'pk': comment.pk}
    url = reverse(url_name, kwargs=kwargs)
    response = client.get(url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse(expected_redirect_url_name))


def test_comment_edit_delete_accessible_to_author(
        client,
        comment_factory,
        news_factory,
        user_factory
):
    user = user_factory(username='author_user')
    client.force_login(user)
    news = news_factory()
    comment = comment_factory(news=news, author=user)
    edit_url = reverse('news:edit', kwargs={'pk': comment.pk})
    delete_url = reverse('news:delete', kwargs={'pk': comment.pk})

    response_edit = client.get(edit_url)
    response_delete = client.get(delete_url)
    assert response_edit.status_code == HTTPStatus.OK
    assert response_delete.status_code == HTTPStatus.OK


def test_user_cannot_edit_or_delete_other_users_comments(
        client,
        comment_factory,
        news_factory,
        user_factory
):
    other_user = user_factory(username='other_user')
    client.force_login(other_user)
    news = news_factory()
    comment = comment_factory(news=news)
    edit_url = reverse('news:edit', kwargs={'pk': comment.pk})
    delete_url = reverse('news:delete', kwargs={'pk': comment.pk})

    response_edit = client.get(edit_url)
    response_delete = client.get(delete_url)
    assert response_edit.status_code == HTTPStatus.NOT_FOUND
    assert response_delete.status_code == HTTPStatus.NOT_FOUND
