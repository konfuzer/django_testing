import pytest
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from news.models import Comment, News


User = get_user_model()


class Constants:
    COMMENT_TEXT = 'Comment_text'
    EDITED_COMMENT = 'Edited Comment'
    OTHER_COMMENT = 'Other User Comment'


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def urls(setup_news):
    return {
        'home': reverse('news:home'),
        'news_detail': reverse('news:detail', kwargs={'pk': setup_news.pk}),
        'users_login': reverse('users:login'),
        'users_logout': reverse('users:logout'),
        'users_signup': reverse('users:signup'),
        'news_edit': reverse('news:edit', kwargs={'pk': 1}),
        'news_delete': reverse('news:delete', kwargs={'pk': 1}),
    }


@pytest.fixture
def delete_comment_url(comment):
    return reverse('news:delete', kwargs={'pk': comment.pk})


@pytest.fixture
def delete_url(comment):
    return {
        'url': reverse('news:delete', kwargs={'pk': comment.pk}),
        'comment': comment
    }


@pytest.fixture
def edit_other_comment_url(other_comment):
    return reverse('news:edit', kwargs={'pk': other_comment.pk})


@pytest.fixture
def news_factory(db):
    def create_news(**kwargs):
        return News.objects.create(
            title=kwargs.get('title', 'Test Title'),
            text=kwargs.get('text', 'Test news text'),
            date=kwargs.get('date', '2023-01-01'),
        )
    return create_news


@pytest.fixture
def comment_factory(user_factory):
    def create_comment(news, author=None, text="Test comment"):
        if not author:
            author = user_factory()
        comment = Comment.objects.create(news=news, author=author, text=text)
        return comment
    return create_comment


@pytest.fixture
def user_factory():
    def create_user(username=None, password='password123'):
        if username is None:
            # Генерируем уникальное имя пользователя
            username = f'testuser_{uuid.uuid4()}'
        return User.objects.create_user(
            username=username,
            password=password,
        )
    return create_user


@pytest.fixture
def ordered_news(setup_news):
    news1 = News.objects.create(date='2023-01-01')
    news2 = setup_news
    return news1, news2


@pytest.fixture
def comments_for_news(setup_news, user_factory):
    user = user_factory()
    comment_old = Comment.objects.create(
        news=setup_news, author=user, text='Older comment')
    comment_newer = Comment.objects.create(
        news=setup_news, author=user, text="Newer Test comment")
    return comment_old, comment_newer


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
def comment(news, author_user):
    return Comment.objects.create(
        news=news,
        author=author_user,
        text="Test Comment"
    )


@pytest.fixture
def multiple_news(news_factory):
    def create_multiple_news(count=settings.NEWS_COUNT_ON_HOME_PAGE):
        news_list = [news_factory() for _ in range(count)]
        return news_list
    return create_multiple_news


@pytest.fixture
def other_comment(db, news, other_user):
    return Comment.objects.create(
        news=news,
        author=other_user,
        text='Other User Comment'
    )


@pytest.fixture
def setup_news(db):
    return News.objects.create(title='Test News', text='Some content')


@pytest.fixture
def setup_comment(client, user_factory, comment_factory, news):
    user = user_factory(username='author_user')
    client.force_login(user)
    comment = comment_factory(news=news, author=user)
    return {
        'user': user,
        'comment': comment,
        'edit_url': reverse('news:edit', kwargs={'pk': comment.pk}),
        'delete_url': reverse('news:delete', kwargs={'pk': comment.pk}),
    }


@pytest.fixture
def other_user_comment(client, other_user, comment_factory, news):
    client.force_login(other_user)
    comment = comment_factory(news=news, author=other_user)
    return {
        'comment': comment,
        'edit_url': reverse('news:edit', kwargs={'pk': comment.pk}),
        'delete_url': reverse('news:delete', kwargs={'pk': comment.pk}),
    }
