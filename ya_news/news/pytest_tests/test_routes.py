import pytest
from django.urls import reverse
from news.models import News, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user_factory(db):
    def create_user(**kwargs):
        return User.objects.create(**kwargs)
    return create_user


@pytest.fixture
def news_factory(db):
    def create_news(**kwargs):
        return News.objects.create(**kwargs)
    return create_news


@pytest.fixture
def comment_factory(db, user_factory, news_factory):
    def create_comment(**kwargs):
        author = kwargs.get('author', user_factory(username='testuser'))
        news = kwargs.get('news', news_factory(
            title='Test News', text='Some news text'))
        return Comment.objects.create(author=author, news=news, text=kwargs.get('text', 'Default comment text'))
    return create_comment


@pytest.mark.django_db
def test_homepage_accessible_to_anonymous(client):
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_news_detail_accessible_to_anonymous(client, news_factory):
    news = news_factory()
    url = reverse('news:detail', kwargs={'pk': news.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_comment_edit_delete_accessible_to_author(client, comment_factory, user_factory):
    user = user_factory(username='author_user')
    client.force_login(user)
    comment = comment_factory(author=user)
    edit_url = reverse('news:edit', kwargs={'pk': comment.pk})
    delete_url = reverse('news:delete', kwargs={'pk': comment.pk})

    response_edit = client.get(edit_url)
    response_delete = client.get(delete_url)
    assert response_edit.status_code == 200
    assert response_delete.status_code == 200


@pytest.mark.django_db
def test_anonymous_redirected_on_comment_edit_delete(client, comment_factory):
    comment = comment_factory()
    edit_url = reverse('news:edit', kwargs={'pk': comment.pk})
    delete_url = reverse('news:delete', kwargs={'pk': comment.pk})

    response_edit = client.get(edit_url)
    response_delete = client.get(delete_url)
    assert response_edit.status_code == 302
    assert response_delete.status_code == 302
    assert response_edit.url.startswith(reverse('login'))
    assert response_delete.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_user_cannot_edit_or_delete_other_users_comments(client, comment_factory, user_factory):
    other_user = user_factory(username='other_user')
    client.force_login(other_user)
    comment = comment_factory()  # Комментарий принадлежит другому пользователю
    edit_url = reverse('news:edit', kwargs={'pk': comment.pk})
    delete_url = reverse('news:delete', kwargs={'pk': comment.pk})

    response_edit = client.get(edit_url)
    response_delete = client.get(delete_url)
    assert response_edit.status_code == 404
    assert response_delete.status_code == 404


@pytest.mark.django_db
def test_auth_pages_accessible_to_anonymous(client):
    login_url = reverse('login')
    logout_url = reverse('logout')
    signup_url = reverse('signup')

    assert client.get(login_url).status_code == 200
    assert client.get(logout_url).status_code == 200
    assert client.get(signup_url).status_code == 200
