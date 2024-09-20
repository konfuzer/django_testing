import pytest

from django.conf import settings

from news.forms import CommentForm


pytestmark = pytest.mark.django_db


def test_homepage_news_count(client, multiple_news, urls):
    multiple_news()
    response = client.get(urls['home'])
    assert response.context['object_list'].count() == \
        settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order_on_homepage(client, ordered_news, urls):
    news1, news2 = ordered_news
    response = client.get(urls['home'])
    assert list(response.context['object_list']) == [news2, news1]


def test_comment_order_on_news_detail(client, comments_for_news, urls):
    comment_old, comment_newer = comments_for_news
    response = client.get(urls['news_detail'])
    assert list(response.context['object'].comment_set.all()) == [
        comment_old, comment_newer]


def test_anonymous_cannot_see_comment_form(client, urls):
    response = client.get(urls['news_detail'])
    assert 'form' not in response.context


def test_authorized_user_can_see_comment_form(
    author_client,
    urls
):
    response = author_client.get(urls['news_detail'])
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
