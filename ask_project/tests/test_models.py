from django.test import TestCase

import datetime
import mock
from django.contrib.auth.models import User
from django.utils import timezone
from ask_project.models import *


# Test Model Profile
class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User()
        user.save()
        user.username = 'testuser'
        user.first_name = 'testuser_firstname'
        user.last_name = 'testuser_lastname'
        user.email = 'testuser' + '@mail.ru'
        user.password = 'testuser'
        user.is_active = True
        user.is_superuser = False
        user.save()
        user_data = Profile()
        user_data.user = user
        user_data.save()

    # INTEGRATIONS TEST
    def test_profile_model_username_exist(self):
        profile = Profile.objects.get(id=1).user
        field_username = profile._meta.get_field('username').verbose_name
        self.assertEquals(field_username, 'username')

    def test_profile_model_username_value(self):
        profile = Profile.objects.get(id=1).user
        self.assertEquals(profile.username, 'testuser')

    def test_profile_model_email_exist(self):
        profile = Profile.objects.get(id=1).user
        field_username = profile._meta.get_field('email').verbose_name
        self.assertEquals(field_username, 'email address')

    def test_profile_model_email_value(self):
        profile = Profile.objects.get(id=1).user
        self.assertEquals(profile.email, 'testuser@mail.ru')

    def test_profile_model_password_exist(self):
        profile = Profile.objects.get(id=1).user
        field_username = profile._meta.get_field('password').verbose_name
        self.assertEquals(field_username, 'password')

    def test_profile_model_first_name_exist(self):
        profile = Profile.objects.get(id=1).user
        field_first_name = profile._meta.get_field('first_name').verbose_name
        self.assertEquals(field_first_name, 'first name')

    def test_profile_model_first_name_value(self):
        profile = Profile.objects.get(id=1).user
        self.assertEquals(profile.first_name, 'testuser_firstname')

    def test_profile_model_last_name_exist(self):
        profile = Profile.objects.get(id=1).user
        field_last_name = profile._meta.get_field('last_name').verbose_name
        self.assertEquals(field_last_name, 'last name')

    def test_profile_model_last_name_value(self):
        profile = Profile.objects.get(id=1).user
        self.assertEquals(profile.last_name, 'testuser_lastname')

    def test_profile_model_avatar_exist(self):
        profile = Profile.objects.get(id=1)
        field_username = profile._meta.get_field('avatar').verbose_name
        self.assertEquals(field_username, 'avatar')

    def test_profile_model_avatar_url_default(self):
        profile = Profile.objects.get(id=1)
        self.assertEquals(profile.avatar.url, '/uploads/avatars/no-frame.png')


class ProfileModelTestMock(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User()
        user.save()
        user.username = 'testuser1'
        user.first_name = 'testuser_firstname'
        user.last_name = 'testuser_lastname'
        user.email = 'testuser1' + '@mail.ru'
        user.password = 'testuser'
        user.is_active = True
        user.is_superuser = False
        user.save()
        user_data = Profile()
        user_data.user = user
        user_data.save()

    @mock.patch('ask_project.models.Profile')
    def test_profile_model_avatar_url_mock(self, mock_utils):
        user = User()
        user.save()
        user.username = 'testuser'
        user.first_name = 'testuser_firstname'
        user.last_name = 'testuser_lastname'
        user.email = 'testuser' + '@mail.ru'
        user.password = 'testuser'
        user.is_active = True
        user.is_superuser = False
        user.save()
        mock_utils.avatar = 'default'
        mock_utils.user = user
        self.assertEqual(mock_utils.avatar, 'default')

    @mock.patch('ask_project.models.Profile.objects.get')
    def test_request_response_with_decorator1(self, mock_get):
        mock_get.return_value.avatar = 'deff'
        response = Profile.objects.get(id = 1)
        self.assertEqual(response.avatar, 'deff')

    @mock.patch('ask_project.models.Profile.objects.get')
    def test_request_response_with_decorator2(self, mock_get):
        mock_get.return_value.user.username = 'deff'
        response = Profile.objects.get(id = 1).user
        self.assertEqual(response.username, 'deff')

    @mock.patch('ask_project.models.Profile.objects.get')
    def test_request_response_with_decorator3(self, mock_get):
        mock_get.return_value.user.first_name = 'deff'
        response = Profile.objects.get(id = 1).user
        self.assertEqual(response.first_name, 'deff')

    @mock.patch('ask_project.models.Profile.objects.get')
    def test_request_response_with_decorator4(self, mock_get):
        mock_get.return_value.user.last_name = 'deff'
        response = Profile.objects.get(id = 1).user
        self.assertEqual(response.last_name, 'deff')

    @mock.patch('ask_project.models.Profile.objects.get')
    def test_request_response_with_decorator5(self, mock_get):
        mock_get.return_value.user.email = 'deff@mail.ru'
        response = Profile.objects.get(id = 1).user
        self.assertEqual(response.email, 'deff@mail.ru')

    '''
    class BasicTests(unittest.TestCase):
        @patch('users.requests.get')  # Mock 'requests' module 'get' method.
        def test_request_response_with_decorator(self, mock_get):
            """Mocking using a decorator"""
            mock_get.return_value.status_code = 200 # Mock status code of response.
            response = get_users()
    
            # Assert that the request-response cycle completed successfully.
            self.assertEqual(response.status_code, 200)
    '''

    '''
    @mock.patch('django.contrib.auth.models.User')
    def test_user_model_avatar_url_mock(self, mock_utils):
        print(mock_utils.email)
        m = mock_utils()
        print(m)
        profile = Profile()
        profile.user = mock_utils
        self.assertEqual(profile.user.username, 'testuser')
    
    @patch('models.Po.sum', return_value=9)
    def test_sum(self, sum):
        self.assertEqual(sum(2,3), 9)
    def test_profile_model_email_value_mock(self):
        print(user.username)
        #profile = Profile.objects.get(id=1)
        #self.assertEquals(profile.last_name, 'testuser_lastname')
    '''


class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User()
        user.save()
        user.username = 'testuser'
        user.first_name = 'testuser_firstname'
        user.last_name = 'testuser_lastname'
        user.email = 'testuser' + '@mail.ru'
        user.password = 'testuser'
        user.is_active = True
        user.is_superuser = False
        user.save()
        user_data = Profile()
        user_data.user = user
        user_data.save()

        question = Question()
        question.title = 'testquestion_title'
        question.text = 'testquestion_text'
        question.author = Profile.objects.get(id=1)
        question.save()


'''
     question = Question()
      question.title = choice(question_title)
      question.text = choice(question_text)
      question.author = choice(users)
      question.save()

      count_tags = randint(1, 3)
      for i in range(count_tags):
        tag_obj = Tag.objects.get_or_create(choice(tags_name))
        question.tags.add(tag_obj)
'''
