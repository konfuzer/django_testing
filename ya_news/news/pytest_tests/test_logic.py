import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

from ..models import News, Comment


@pytest.mark.django_db
def test_anonymous_user_cannot_submit_comment(client, news):
    response = client.post(
        reverse('news:detail', kwargs={'pk': news.pk}),
        {'text': 'Test Comment'}
    )
    assert response.status_code == 302
    assert response.url.startswith(reverse('account_login'))


@pytest.mark.django_db
def test_authorized_user_can_submit_comment(author_client, news):
    response = author_client.post(
        reverse('news:detail', kwargs={'pk': news.pk}),
        {'text': 'Test Comment'}
    )
    assert response.status_code == 302
    assert news.comment_set.count() == 1


@pytest.mark.django_db
def test_cannot_submit_comment_with_bad_words(author_client, news):
    response = author_client.post(
        reverse('news:detail', kwargs={'pk': news.pk}),
        {'text': 'редиска'}
    )
    assert response.status_code == 200
    assert 'Не ругайтесь!' in response.content.decode()


@pytest.mark.django_db
def test_authorized_user_can_edit_delete_own_comment(author_client, comment):
    edit_url = reverse('news:edit', kwargs={'pk': comment.pk})
    response = author_client.post(edit_url, {'text': 'Edited Comment'})
    assert response.status_code == 302
    comment.refresh_from_db()
    assert comment.text == 'Edited Comment'


@pytest.mark.django_db
def test_cannot_edit_delete_other_users_comment(other_user_client, comment):
    edit_url = reverse('news:edit', kwargs={'pk': comment.pk})
    response = other_user_client.post(edit_url, {'text': 'Hacked Comment'})
    assert response.status_code == 403


@pytest.fixture
def news(db):
    return News.objects.create(title="Test News", text="Some content")


@pytest.fixture
def author_user(db):
    return User.objects.create_user(username="author", password="password")


@pytest.fixture
def author_client(db, author_user):
    client = Client()
    client.login(username="author", password="password")
    return client


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="other", password="password")


@pytest.fixture
def other_user_client(db, other_user):
    client = Client()
    client.login(username="other", password="password")
    return client


@pytest.fixture
def comment(db, news, author_user):
    return Comment.objects.create(news=news,
                                  user=author_user,
                                  text="Test Comment")
