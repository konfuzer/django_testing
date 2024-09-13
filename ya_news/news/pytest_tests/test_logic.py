import pytest
from django.urls import reverse


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


@pytest.mark.django_db
def test_cannot_submit_comment_with_bad_words(author_client, news):
    response = author_client.post(
        reverse('news:detail', kwargs={'pk': news.pk}),
        {'text': 'редиска'}
    )
    assert response.status_code == 200
    assert 'Не ругайтесь!' in response.content.decode()


@pytest.mark.django_db
def test_authorized_user_can_edit_delete_own_comment(author_client, comment):
    edit_url = reverse('news:edit', kwargs={'pk': comment.pk})
    response = author_client.post(edit_url, {'text': 'Edited Comment'})
    assert response.status_code == 302
    comment.refresh_from_db()
    assert comment.text == 'Edited Comment'


@pytest.mark.django_db
def test_cannot_edit_delete_other_users_comment(other_user_client, comment):
    edit_url = reverse('news:edit', kwargs={'pk': comment.pk})
    response = other_user_client.post(edit_url, {'text': 'Hacked Comment'})
    assert response.status_code == 403
