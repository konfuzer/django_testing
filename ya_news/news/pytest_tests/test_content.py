import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from news.models import News, Comment


@pytest.fixture
def news_factory(db):
    def create_news(**kwargs):
        return News.objects.create(
            title=kwargs.get('title', 'Test Title'),
            date=kwargs.get('date', '2023-01-01'),
        )
    return create_news


@pytest.fixture
def comment_factory(db):
    def create_comment(news, **kwargs):
        return Comment.objects.create(
            text=kwargs.get('text', 'Test comment'),
            created=kwargs.get('created', '2023-01-01'),
            news=news
        )
    return create_comment


@pytest.fixture
def user_factory(db):
    def create_user(**kwargs):
        User = get_user_model()
        return User.objects.create_user(
            username=kwargs.get('username', 'testuser'),
            email=kwargs.get('email', 'test@example.com'),
            password=kwargs.get('password', 'password123')
        )
    return create_user


@pytest.mark.django_db
def test_homepage_news_count(client, news_factory, settings):
    settings.NEWS_COUNT_ON_HOME_PAGE = 10
    for _ in range(15):
        news_factory()
    response = client.get(reverse('news:home'))
    assert len(response.context['object_list']) <= 10


@pytest.mark.django_db
def test_news_order_on_homepage(client, news_factory):
    news1 = news_factory(date='2022-01-01')
    news2 = news_factory(date='2023-01-01')
    response = client.get(reverse('news:home'))
    assert list(response.context['object_list']) == [news2, news1]


@pytest.mark.django_db
def test_comment_order_on_news_detail(client, news_factory, comment_factory):
    news = news_factory()
    comment_old = comment_factory(news=news, created='2023-01-01')
    comment_new = comment_factory(news=news, created='2024-01-01')
    response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    assert list(response.context['news'].comment_set.all()) == [
        comment_old, comment_new]


@pytest.mark.django_db
def test_anonymous_cannot_see_comment_form(client, news_factory):
    news = news_factory()
    response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_user_can_see_comment_form(client, news_factory, user_factory):
    user = user_factory()
    client.force_login(user)
    news = news_factory()
    response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    assert 'form' in response.context
