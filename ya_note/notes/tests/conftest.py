from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.forms import WARNING


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


class BaseTestCase(TestCase):
    """Базовый тестовый класс с фикстурами и реверсами URL."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username=Constants.USERNAME_1, password=Constants.PASSWORD_1
        )
        cls.other_user = User.objects.create_user(
            username=Constants.USERNAME_2, password=Constants.PASSWORD_2
        )

        cls.note = Note.objects.create(
            title=Constants.TEST_NOTE_TITLE,
            text=Constants.TEST_NOTE_TEXT,
            author=cls.user,
            slug=Constants.TEST_NOTE_SLUG
        )

        cls.home_url = reverse('notes:home')

        cls.notes_list_url = reverse('notes:list')

        cls.add_url = reverse('notes:add')

        cls.detail_url = reverse(
            'notes:detail', kwargs={'slug': Constants.TEST_NOTE_SLUG}
        )
        cls.edit_url = reverse(
            'notes:edit', kwargs={'slug': Constants.TEST_NOTE_SLUG}
        )
        cls.delete_url = reverse(
            'notes:delete', kwargs={'slug': Constants.TEST_NOTE_SLUG}
        )
        cls.login_url = reverse('users:login')

        cls.client_testuser = cls.client_class()

        cls.client_testuser.login(
            username=Constants.USERNAME_1, password=Constants.PASSWORD_1
        )

        cls.client_otheruser = cls.client_class()

        cls.client_otheruser.login(
            username=Constants.USERNAME_2, password=Constants.PASSWORD_2
        )

        cls.new_note_data = {
            'title': Constants.NEW_NOTE_TITLE,
            'text': Constants.NEW_NOTE_TEXT,
            'slug': Constants.NEW_NOTE_SLUG
        }

        cls.edit_note_data = {
            'title': Constants.EDITED_NOTE_TITLE,
            'text': Constants.EDITED_NOTE_TEXT,
            'slug': Constants.TEST_NOTE_SLUG
        }

        cls.hacked_note_data = {
            'title': Constants.HACKED_NOTE_TITLE,
            'text': Constants.HACKED_NOTE_TEXT,
            'slug': Constants.TEST_NOTE_SLUG
        }

        cls.duplicate_slug_data = {
            'title': Constants.ANOTHER_NOTE_TITLE,
            'text': Constants.ANOTHER_NOTE_TEXT,
            'slug': Constants.TEST_NOTE_SLUG
        }

        cls.generated_note_data = {
            'title': Constants.GENERATED_NOTE_TITLE,
            'text': Constants.GENERATED_NOTE_TEXT
        }

        cls.duplicate_slug_error = Constants.TEST_NOTE_SLUG + WARNING
