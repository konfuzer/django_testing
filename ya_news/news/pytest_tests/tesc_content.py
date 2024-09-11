import pytest
from django.urls import reverse
from news.models import News, Comment


@pytest.mark.django_db
def test_news_count_on_home_page(client, news_factory):
    response = client.get(reverse('news:home'))
    assert len(response.context['object_list']) <= 10


@pytest.mark.django_db
def test_news_sorted_by_date(client, news_factory):
    response = client.get(reverse('news:home'))
    news_list = response.context['object_list']
    assert list(news_list) == sorted(news_list,
                                     key=lambda x: x.date,
                                     reverse=True)


@pytest.mark.django_db
def test_comments_ordered_on_news_detail(client, news, comment_factory):
    response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    comments = response.context['news'].comment_set.all()
    assert list(comments) == sorted(comments, key=lambda x: x.created)


@pytest.mark.django_db
def test_comment_form_visibility_for_anonymous(client, news):
    response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    assert 'form' not in response.context


@pytest.mark.django_db
def test_comment_form_visibility_for_authenticated(client, news, user):
    client.force_login(user)
    response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    assert 'form' in response.context
