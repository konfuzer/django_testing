import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_page_accessible(client):
    response = client.get(reverse('news:home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_news_detail_accessible(client, django_assert_num_queries, news):
    with django_assert_num_queries(5):
        response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_comment_edit_delete_accessible_to_author(client, author, comment):
    client.force_login(author)
    edit_url = reverse('news:edit', kwargs={'pk': comment.pk})
    response = client.get(edit_url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_anonymous_redirected_to_login(client, comment):
    edit_url = reverse('news:edit', kwargs={'pk': comment.pk})
    response = client.get(edit_url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('account_login'))


@pytest.mark.django_db
def test_other_user_cannot_access_edit_delete(client, another_user, comment):
    client.force_login(another_user)
    edit_url = reverse('news:edit', kwargs={'pk': comment.pk})
    response = client.get(edit_url)
    assert response.status_code == 403
