import pytest
from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cannot_submit_comment(client, news):
    response = client.post(
        reverse('news:detail', kwargs={'pk': news.pk}),
        {'text': 'Test Comment'}
    )
    assert response.status_code == 302
    assert response.url.startswith(reverse('users:login'))
    # Проверяем количество комментариев
    assert Comment.objects.filter(news=news).count() == 0


@pytest.mark.django_db
def test_authorized_user_can_submit_comment(author_client, news):
    initial_count = Comment.objects.filter(news=news).count()
    response = author_client.post(
        reverse('news:detail', kwargs={'pk': news.pk}),
        {'text': 'Test Comment'}
    )
    assert response.status_code == 302
    assert Comment.objects.filter(news=news).count() == initial_count + 1


@pytest.mark.django_db
def test_cannot_submit_comment_with_bad_words(author_client, news):
    response = author_client.post(
        reverse('news:detail', kwargs={'pk': news.pk}),
        {'text': BAD_WORDS}
    )
    assert response.status_code == 200
    assert WARNING in response.content.decode()


@pytest.mark.django_db
def test_authorized_user_cannot_edit_delete_other_comment(
    author_client,
    other_user,
    news
):
    other_comment = Comment.objects.create(
        news=news,
        author=other_user,
        text='Other User Comment'
    )
    edit_url = reverse('news:edit', kwargs={'pk': other_comment.pk})
    response = author_client.post(edit_url, {'text': 'Edited Comment'})

    # Проверяем, что URL действительно существует
    assert response.status_code != 404
    # Проверяем, что статус 403 при редактировании чужого комментария
    assert response.status_code == 403

    delete_url = reverse('news:delete', kwargs={'pk': other_comment.pk})
    response = author_client.post(delete_url)
    assert response.status_code != 404

    # Проверяем, что статус 403 при удалении чужого комментария
    assert response.status_code == 403


@pytest.mark.django_db
def test_authorized_user_can_delete_own_comment(author_client, comment):
    delete_url = reverse('news:delete', kwargs={'pk': comment.pk})
    response = author_client.post(delete_url)
    assert response.status_code == 302
    assert Comment.objects.filter(pk=comment.pk).count() == 0


@pytest.mark.django_db
def test_authorized_user_cannot_edit_delete_other_comment(
    author_client,
    other_user,
    news
):
    other_comment = Comment.objects.create(
        news=news,
        author=other_user,
        text='Other User Comment'
    )
    edit_url = reverse('news:edit', kwargs={'pk': other_comment.pk})

    assert Comment.objects.filter(pk=other_comment.pk).exists()

    response = author_client.post(edit_url, {'text': 'Edited Comment'})

    assert response.status_code == 404
