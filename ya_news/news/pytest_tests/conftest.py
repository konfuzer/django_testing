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
def urls(news, comment, other_comment):
    return {
        'home': reverse('news:home'),
        'news_detail': reverse('news:detail', kwargs={'pk': news.pk}),
        'users_login': reverse('users:login'),
        'users_logout': reverse('users:logout'),
        'users_signup': reverse('users:signup'),
        'news_edit': reverse('news:edit', kwargs={'pk': comment.pk}),
        'news_delete': reverse('news:delete', kwargs={'pk': comment.pk}),
        'edit_other': reverse('news:edit', kwargs={'pk': other_comment.pk}),
        'delete_other': reverse(
            'news:delete',
            kwargs={'pk': other_comment.pk}
        ),
    }


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
def multiple_news(news_factory):
    def create_multiple_news(count=settings.NEWS_COUNT_ON_HOME_PAGE):
        return [news_factory() for _ in range(count)]
    return create_multiple_news


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
            username = f'testuser_{uuid.uuid4()}'
        return User.objects.create_user(
            username=username,
            password=password,
        )
    return create_user


@pytest.fixture
def comments_for_news(news, user_factory):
    user = user_factory()
    comment_old = Comment.objects.create(
        news=news, author=user, text='Older comment')
    comment_newer = Comment.objects.create(
        news=news, author=user, text="Newer Test comment")
    return comment_old, comment_newer


@pytest.fixture
def news(db):
    return News.objects.create(title="Test News", text="Some content")


@pytest.fixture
def author_user(db):
    return User.objects.create_user(username="author", password="password")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="other", password="password")


@pytest.fixture
def comment(news, author_user):
    return Comment.objects.create(
        news=news,
        author=author_user,
        text="Test Comment"
    )


@pytest.fixture
def other_comment(db, news, other_user):
    return Comment.objects.create(
        news=news,
        author=other_user,
        text='Other User Comment'
    )


@pytest.fixture
def author_client(db, author_user):
    client = Client()
    client.login(username="author", password="password")
    return client
