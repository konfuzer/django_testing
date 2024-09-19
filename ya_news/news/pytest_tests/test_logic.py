import pytest

from http import HTTPStatus

from news.forms import WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cannot_submit_comment(
    client,
    news,
    urls,
    comment_text
):
    initial_comment_count = Comment.objects.filter(news=news).count()

    response = client.post(urls['news_detail'], {'text': comment_text})

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(urls['users_login'])
    assert Comment.objects.filter(news=news).count() == initial_comment_count


@pytest.mark.django_db
def test_authorized_user_can_submit_comment(
    author_client,
    author_user,
    news,
    detail_url,
    comment_text
):
    initial_count = Comment.objects.filter(news=news).count()

    response = author_client.post(detail_url, {'text': comment_text})

    assert response.status_code == HTTPStatus.FOUND

    assert Comment.objects.filter(news=news).count() == initial_count + 1

    last_comment = Comment.objects.filter(news=news).latest('created')
    assert last_comment.text == comment_text
    assert last_comment.author == author_user
    assert last_comment.news == news


@pytest.mark.django_db
def test_cannot_submit_comment_with_bad_words(
    author_client,
    detail_url,
    bad_words
):
    response = author_client.post(detail_url, {'text': bad_words})
    assert response.status_code == HTTPStatus.OK
    assert WARNING in response.content.decode()


@pytest.mark.django_db
def test_authorized_user_cannot_edit_delete_other_comment(
    author_client,
    other_comment,
    edit_url,
    other_comment_text,
    updated_comment_text
):
    assert Comment.objects.filter(pk=other_comment.pk).exists()
    response = author_client.post(edit_url, {'text': updated_comment_text})
    assert response.status_code == HTTPStatus.NOT_FOUND
    other_comment.refresh_from_db()
    assert other_comment.text == other_comment_text


@pytest.mark.django_db
def test_authorized_user_can_delete_own_comment(
        author_client,
        delete_url,
        comment
):
    initial_count = Comment.objects.filter(news=comment.news).count()

    response = author_client.post(delete_url['url'])
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.filter(
        news=comment.news).count() == initial_count - 1
