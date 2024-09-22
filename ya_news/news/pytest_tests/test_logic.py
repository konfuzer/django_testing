import pytest
from http import HTTPStatus

from conftest import Constants
from news.forms import BAD_WORDS, WARNING
from news.models import Comment


pytestmark = pytest.mark.django_db


def test_anonymous_user_cannot_submit_comment(
    client,
    news,
    urls,
):
    initial_comment_count = Comment.objects.filter(news=news).count()

    response = client.post(urls['news_detail'], {
                           'text': Constants.COMMENT_TEXT})

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(urls['users_login'])
    assert Comment.objects.filter(news=news).count() == initial_comment_count


def test_authorized_user_can_submit_comment(
    author_client,
    author_user,
    news,
    urls
):
    Comment.objects.all().delete()

    initial_count = Comment.objects.filter(news=news).count()
    response = author_client.post(
        urls['news_detail'], {'text': Constants.COMMENT_TEXT})
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.filter(news=news).count() == initial_count + 1
    last_comment = Comment.objects.get()
    assert last_comment.text == Constants.COMMENT_TEXT
    assert last_comment.author == author_user
    assert last_comment.news == news


def test_cannot_submit_comment_with_bad_words(
    author_client,
    urls
):
    response = author_client.post(urls['news_detail'], {'text': BAD_WORDS})
    assert response.status_code == HTTPStatus.OK
    assert WARNING in response.content.decode()


def test_authorized_user_cannot_edit_other_comment(
    author_client,
    other_comment,
    urls
):
    assert Comment.objects.filter(pk=other_comment.pk).exists()
    response = author_client.post(urls['edit_other'], {
                                  'text': Constants.EDITED_COMMENT})
    assert response.status_code == HTTPStatus.NOT_FOUND
    retrieved_comment = Comment.objects.get(pk=other_comment.pk)
    assert retrieved_comment.text == Constants.OTHER_COMMENT
    assert retrieved_comment.author == other_comment.author
    assert retrieved_comment.news == other_comment.news


def test_authorized_user_can_delete_own_comment(
        author_client,
        comment,
        urls
):
    initial_count = Comment.objects.filter(news=comment.news).count()

    response = author_client.post(urls['news_delete'])
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.filter(
        news=comment.news).count() == initial_count - 1


def test_authorized_user_can_edit_own_comment(
    author_client,
    comment,
    urls,
):
    response = author_client.post(
        urls['news_edit'], {'text': Constants.EDITED_COMMENT}
    )

    assert response.status_code == HTTPStatus.FOUND

    retrieved_comment = Comment.objects.get(pk=comment.pk)

    assert retrieved_comment.pk == comment.pk
    assert retrieved_comment.news == comment.news
    assert retrieved_comment.author == comment.author
    assert retrieved_comment.created == comment.created
    assert retrieved_comment.text == Constants.EDITED_COMMENT


def test_authorized_user_cannot_delete_other_comment(
    author_client, other_comment, urls
):
    initial_count = Comment.objects.filter(news=other_comment.news).count()

    response = author_client.post(urls['delete_other'])
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.filter(
        news=other_comment.news).count() == initial_count
