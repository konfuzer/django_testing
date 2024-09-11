import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_home_page_accessible(client):
    response = client.get(reverse('news:home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_news_detail_accessible(client, django_assert_num_queries, news):
    response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_comment_edit_delete_accessible_to_author(client, author, comment):
    client.force_login(author)
    response = client.get(reverse('news:edit', kwargs={'pk': comment.pk}))
    assert response.status_code == 200

    response = client.get(reverse('news:delete', kwargs={'pk': comment.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_anonymous_redirected_to_login(client, comment):
    response = client.get(reverse('news:edit', kwargs={'pk': comment.pk}))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

    response = client.get(reverse('news:delete', kwargs={'pk': comment.pk}))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_other_user_cannot_access_edit_delete(client, another_user, comment):
    client.force_login(another_user)
    response = client.get(reverse('news:edit', kwargs={'pk': comment.pk}))
    assert response.status_code == 404

    response = client.get(reverse('news:delete', kwargs={'pk': comment.pk}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_registration_login_logout_accessible_to_anonymous(client):
    response = client.get(reverse('register'))
    assert response.status_code == 200

    response = client.get(reverse('login'))
    assert response.status_code == 200

    response = client.get(reverse('logout'))
    assert response.status_code == 200
