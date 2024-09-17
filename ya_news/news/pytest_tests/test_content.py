import pytest
from django.urls import reverse

from news.forms import CommentForm
from news.models import Comment


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
def test_comment_order_on_news_detail(client, news_factory, user_factory):
    user = user_factory()
    news = news_factory()
    comment_old = Comment.objects.create(
        news=news,
        author=user,
        text='Older comment',
    )
    comment_newer = Comment.objects.create(
        news=news,
        author=user,
        text="Newer Test comment",
    )
    comments = list(Comment.objects.filter(news=news).order_by('created'))
    assert comments == [comment_old, comment_newer]


@pytest.mark.django_db
def test_anonymous_cannot_see_comment_form(client, news_factory):
    news = news_factory()
    response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_user_can_see_comment_form(
    client,
    user_factory,
    news_factory
):
    user = user_factory()
    client.force_login(user)
    news = news_factory()
    response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
