import pytest

from news.forms import CommentForm

from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_homepage_news_count(client, multiple_news, urls):
    multiple_news()
    response = client.get(urls['home'])
    assert response.context['object_list'].count() <= NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order_on_homepage(client, ordered_news, urls):
    news1, news2 = ordered_news
    response = client.get(urls['home'])
    assert list(response.context['object_list']) == [news2, news1]


@pytest.mark.django_db
def test_comment_order_on_news_detail(client, comments_for_news, detail_url):
    comment_old, comment_newer = comments_for_news
    response = client.get(detail_url)
    assert list(response.context['object'].comment_set.all()) == [
        comment_old, comment_newer]


@pytest.mark.django_db
def test_anonymous_cannot_see_comment_form(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_user_can_see_comment_form(
    client,
    user_factory,
    detail_url
):
    user = user_factory()
    client.force_login(user)
    response = client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
