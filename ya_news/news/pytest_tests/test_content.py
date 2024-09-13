import pytest
from django.urls import reverse
from django.contrib.auth.models import User

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


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def author_user(db):
    return User.objects.create_user(username='author', password='password')


@pytest.fixture
def author_client(client, author_user):
    client.force_login(author_user)
    return client


@pytest.fixture
def other_user_client(client, db):
    other_user = User.objects.create_user(
        username='other_user', password='password')
    client.force_login(other_user)
    return client


@pytest.fixture
def news(db):
    return News.objects.create(title="Test News", text="Some content")


@pytest.fixture
def comment(author_user, news):
    return Comment.objects.create(news=news,
                                  author=author_user,
                                  text="Test comment"
                                  )


@pytest.mark.django_db
def test_anonymous_user_cannot_submit_comment(client, news):
    response = client.post(
        reverse('news:detail', kwargs={'pk': news.pk}),
        {'text': 'Test Comment'}
    )
    assert response.status_code == 302
    assert response.url.startswith(reverse('account_login'))


@pytest.mark.django_db
def test_authorized_user_can_submit_comment(author_client, news):
    response = author_client.post(
        reverse('news:detail', kwargs={'pk': news.pk}),
        {'text': 'Test Comment'}
    )
    assert response.status_code == 302
    assert news.comment_set.count() == 1
