from django.test import TestCase

import datetime
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

    def test_profile_model_avatar_exist(self):
        profile = Profile.objects.get(id=1)
        field_username = profile._meta.get_field('avatar').verbose_name
        self.assertEquals(field_username, 'avatar')

    def test_profile_model_avatar_url_default(self):
        profile = Profile.objects.get(id=1)
        self.assertEquals(profile.avatar.url, '/uploads/avatars/no-frame.png')




