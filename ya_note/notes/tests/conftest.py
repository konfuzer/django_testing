import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class Constants:
    USERNAME_1 = 'testuser'
    PASSWORD_1 = 'testpass'
    USERNAME_2 = 'otheruser'
    PASSWORD_2 = 'testpass2'
    TEST_NOTE_TITLE = 'Test Note'
    TEST_NOTE_TEXT = 'Test Text'
    TEST_NOTE_SLUG = 'test-note'
    ANOTHER_NOTE_TITLE = 'Another Note'
    ANOTHER_NOTE_TEXT = 'Another Text'
    NEW_NOTE_TITLE = 'New Note'
    NEW_NOTE_TEXT = 'New Text'
    NEW_NOTE_SLUG = 'new-note'
    GENERATED_NOTE_TITLE = 'Generated Slug Note'
    GENERATED_NOTE_TEXT = 'Text'
    EDITED_NOTE_TITLE = 'Edited Note'
    EDITED_NOTE_TEXT = 'Edited Text'
    HACKED_NOTE_TITLE = 'Hacked Note'
    HACKED_NOTE_TEXT = 'Hacked Text'


@pytest.fixture(scope='class')
def base_setup(request):
    user = User.objects.create_user(
        username=Constants.USERNAME_1, password=Constants.PASSWORD_1)
    other_user = User.objects.create_user(
        username=Constants.USERNAME_2, password=Constants.PASSWORD_2)
    note = Note.objects.create(
        title=Constants.TEST_NOTE_TITLE, text=Constants.TEST_NOTE_TEXT, author=user, slug=Constants.TEST_NOTE_SLUG
    )

    request.cls.user = user
    request.cls.other_user = other_user
    request.cls.note = note
    request.cls.add_url = reverse('notes:add')
    request.cls.edit_url = reverse(
        'notes:edit', kwargs={'slug': Constants.TEST_NOTE_SLUG})
    request.cls.delete_url = reverse(
        'notes:delete', kwargs={'slug': Constants.TEST_NOTE_SLUG})
    request.cls.client_testuser = request.cls.client_class()
    request.cls.client_testuser.login(
        username=Constants.USERNAME_1, password=Constants.PASSWORD_1)
    request.cls.client_otheruser = request.cls.client_class()
    request.cls.client_otheruser.login(
        username=Constants.USERNAME_2, password=Constants.PASSWORD_2)
