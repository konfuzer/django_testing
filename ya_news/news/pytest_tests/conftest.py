import pytest
from django.test import Client
from django.contrib.auth import get_user_model

from news.models import News, Comment

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')


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
def user_factory(db):
    def create_user(**kwargs):
        return User.objects.create_user(
            username=kwargs.get('username', 'testuser'),
            email=kwargs.get('email', 'test@example.com'),
            password=kwargs.get('password', 'password123')
        )
    return create_user


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
    return Comment.objects.create(
        news=news,
        author=author_user,
        text="Test Comment"
    )
