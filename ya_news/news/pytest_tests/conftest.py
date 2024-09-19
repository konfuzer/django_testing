import pytest
import uuid

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from news.forms import BAD_WORDS
from news.models import News, Comment
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def urls():
    return {
        'news_detail': reverse('news:detail', kwargs={'pk': 1}),
        'users_login': reverse('users:login'),
        'users_logout': reverse('users:logout'),
        'users_signup': reverse('users:signup'),
        'news_edit': reverse('news:edit', kwargs={'pk': 1}),
        'news_delete': reverse('news:delete', kwargs={'pk': 1}),
        'home': reverse('news:home'),
    }


@pytest.fixture
def delete_comment_url(comment_factory, news_factory):
    news = news_factory()
    comment = comment_factory(news=news)
    return reverse('news:delete', kwargs={'pk': comment.pk})


@pytest.fixture
def delete_url(comment):
    return {
        'url': reverse('news:delete', kwargs={'pk': comment.pk}),
        'comment': comment
    }


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', kwargs={'pk': news.pk})


@pytest.fixture
def edit_comment_url(comment_factory, news_factory):
    news = news_factory()
    comment = comment_factory(news=news)
    return reverse('news:edit', kwargs={'pk': comment.pk})


@pytest.fixture
def edit_url(other_comment):
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
def ordered_news(db, news_factory):
    news1 = news_factory(date='2022-01-01')
    news2 = news_factory(date='2023-01-01')
    return news1, news2


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


@pytest.fixture
def multiple_news(news_factory):
    def create_multiple_news(count=NEWS_COUNT_ON_HOME_PAGE):
        news_list = [news_factory() for _ in range(count)]
        return news_list
    return create_multiple_news


@pytest.fixture
def other_comment(news, other_user):
    return Comment.objects.create(
        news=news,
        author=other_user,
        text='Other User Comment'
    )


@pytest.fixture
def comment_text():
    return "This is a test comment"


@pytest.fixture
def updated_comment_text():
    return "Edited Comment"


@pytest.fixture
def other_comment_text():
    return "Other User Comment"


@pytest.fixture
def bad_words():
    return BAD_WORDS


@pytest.fixture
def setup_news(db):
    news = News.objects.create(title='Test News', text='Some content')
    return news


@pytest.fixture
def setup_comment(client, user_factory, comment_factory):
    user = user_factory(username='author_user')
    client.force_login(user)
    news = News.objects.create(title='Test News', text='Some content')
    comment = comment_factory(news=news, author=user)
    return {
        'user': user,
        'news': news,
        'comment': comment,
        'edit_url': reverse('news:edit', kwargs={'pk': comment.pk}),
        'delete_url': reverse('news:delete', kwargs={'pk': comment.pk}),
    }


@pytest.fixture
def other_user_comment(client, user_factory, comment_factory):
    other_user = user_factory(username='other_user')
    client.force_login(other_user)
    news = News.objects.create(title='Test News', text='Some content')
    comment = comment_factory(news=news)
    return {
        'other_user': other_user,
        'news': news,
        'comment': comment,
        'edit_url': reverse('news:edit', kwargs={'pk': comment.pk}),
        'delete_url': reverse('news:delete', kwargs={'pk': comment.pk}),
    }
