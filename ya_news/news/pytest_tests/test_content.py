import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_homepage_news_count(client, news_factory, settings):
    settings.NEWS_COUNT_ON_HOME_PAGE = 10
    news_factory.create_batch(15)
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
    assert list(response.context['news'].comment_set.all()) == [comment_old,
                                                                comment_new]


@pytest.mark.django_db
def test_anonymous_cannot_see_comment_form(client, news_factory):
    news = news_factory()
    response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_user_can_see_comment_form(client,
                                              news_factory,
                                              user_factory):
    user = user_factory()
    client.force_login(user)
    news = news_factory()
    response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    assert 'form' in response.context
