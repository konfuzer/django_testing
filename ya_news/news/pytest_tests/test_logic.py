import pytest
from django.urls import reverse
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_cannot_post_comment(client, news):
    response = client.post(reverse('news:detail', kwargs={'pk': news.pk}),
                           data={'text': 'Test comment'})
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_authenticated_user_can_post_comment(client, user, news):
    client.force_login(user)
    response = client.post(reverse('news:detail', kwargs={'pk': news.pk}),
                           data={'text': 'Test comment'})
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_comment_with_bad_words_is_rejected(client, user, news):
    client.force_login(user)
    response = client.post(reverse('news:detail', kwargs={'pk': news.pk}),
                           data={'text': 'Ты редиска!'})
    assert response.status_code == 200
    assert 'Не ругайтесь!' in response.context['form'].errors['text']
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_can_edit_own_comment(client, user, comment):
    client.force_login(user)
    response = client.post(reverse('news:edit', kwargs={'pk': comment.pk}),
                           data={'text': 'Updated text'})
    comment.refresh_from_db()
    assert comment.text == 'Updated text'


@pytest.mark.django_db
def test_user_cannot_edit_other_comment(client, another_user, comment):
    client.force_login(another_user)
    response = client.post(reverse('news:edit', kwargs={'pk': comment.pk}),
                           data={'text': 'Hacked text'})
    assert response.status_code == 404
