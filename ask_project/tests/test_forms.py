from django.test import TestCase

# Create your tests here.

import datetime
from django.utils import timezone
from ask_project.forms import *

### MODULE TESTS

# Test form - SignIn
class SignInFormTest(TestCase):
    # Test username fields
    def test_sign_in_form_username_field(self):
        form = SignInForm()
        self.assertTrue(form.fields['username'].label == None or form.fields['username'].label == 'Username')

    def test_sign_in_form_username_max_length_field(self):
        form = SignInForm()
        self.assertTrue(form.fields['username'].widget.attrs['maxlength'], 20)

    def test_sign_in_form_username_min_length_field(self):
        form = SignInForm()
        self.assertTrue(form.fields['username'].widget.attrs['minlength'], 3)

    def test_sign_in_form_username_valid(self):
        form = SignInForm()
        form_widget_attrs = {'class': 'form-control', 'name': 'username'}
        form.fields['username'].widget.attrs = form_widget_attrs
        self.assertFalse(form.is_valid())

    # Test password fields
    def test_sign_in_form_password_field(self):
        form = SignInForm()
        self.assertTrue(form.fields['password'].label == None or form.fields['password'].label == 'Password')

    def test_sign_in_form_password_max_length_field(self):
        form = SignInForm()
        self.assertTrue(form.fields['password'].widget.attrs['maxlength'], 20)

    def test_login_form_password_min_length_field(self):
        form = SignInForm()
        self.assertTrue(form.fields['password'].widget.attrs['minlength'], 4)

    def test_sign_in_form_password_valid(self):
        form = SignInForm()
        form_widget_attrs = {'class': 'form-control', 'name': 'password'}
        form.fields['password'].widget.attrs = form_widget_attrs
        self.assertFalse(form.is_valid())

# Test form - Registration
class RegistrationFormTest(TestCase):
    # Test login fields
    def test_registration_form_login_field(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['login'].label == None or form.fields['login'].label == 'Login')

    def test_registration_form_login_max_length_field(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['login'].widget.attrs['maxlength'], 20)

    def test_registration_form_login_min_length_field(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['login'].widget.attrs['minlength'], 3)

    def test_sign_in_form_login_valid(self):
        form = RegistrationForm()
        form_widget_attrs = {'class': 'form-control', 'name': 'SuperPupkin'}
        form.fields['login'].widget.attrs = form_widget_attrs
        self.assertFalse(form.is_valid())

    # Test email fields
    def test_registration_form_email_field(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['email'].label == None or form.fields['email'].label == 'Email')

    def test_registration_form_email_max_length_field(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['email'].widget.attrs['maxlength'], 255)

    def test_registration_form_email_min_length_field(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['email'].widget.attrs['minlength'], 3)

    def test_sign_in_form_email_valid(self):
        form = RegistrationForm()
        form_widget_attrs = {'class': 'form-control', 'name': 'pupkin@mail.ru'}
        form.fields['email'].widget.attrs = form_widget_attrs
        self.assertFalse(form.is_valid())

    # Test password fields
    def test_registration_form_password_field(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['password'].label == None or form.fields['password'].label == 'Password')

    def test_registration_form_password_max_length_field(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['password'].widget.attrs['maxlength'], 20)

    def test_registration_form_password_min_length_field(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['password'].widget.attrs['minlength'], 4)

    def test_sign_in_form_password_valid(self):
        form = RegistrationForm()
        form_widget_attrs = {'class': 'form-control', 'name': '***********'}
        form.fields['password'].widget.attrs = form_widget_attrs
        self.assertFalse(form.is_valid())


    # Test avatar fields
    def test_registration_form_avatar_field(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['avatar'].label == None or form.fields['avatar'].label == 'Avatar')

# Test form - Question
class AnswerAddFormTest(TestCase):
    # Test text fields
    def test_answer_add_form_text_max_length_field(self):
        form = AnswerAddForm()
        self.assertTrue(form.fields['text'].widget.attrs['maxlength'], 255)

    def test_answer_add_form_text_min_length_field(self):
        form = AnswerAddForm()
        self.assertTrue(form.fields['text'].widget.attrs['minlength'], 3)

    def test_answer_add_form_text_valid(self):
        form = AnswerAddForm()
        form_widget_attrs = {'class': 'form-control', 'name': 'Input text here...', 'rows': 6}
        form.fields['text'].widget.attrs = form_widget_attrs
        self.assertFalse(form.is_valid())

# Test form - Search
class SearchFormTest(TestCase):
    # Test search_word fields
    def test_search_form_search_word_field(self):
        form = SearchForm()
        self.assertTrue(form.fields['search_word'].label == None or form.fields['search_word'].label == 'Search')

    def test_search_form_search_word_max_length_field(self):
        form = SearchForm()
        self.assertTrue(form.fields['search_word'].widget.attrs['maxlength'], 20)

    def test_search_form_search_word_min_length_field(self):
        form = SearchForm()
        self.assertTrue(form.fields['search_word'].widget.attrs['minlength'], 2)

    def test_search_form_search_word_valid(self):
        form = SearchForm()
        form_widget_attrs = {'class': 'form-control', 'name': 'Search'}
        form.fields['search_word'].widget.attrs = form_widget_attrs
        self.assertFalse(form.is_valid())

# Test form - ArticleAdd
class ArticleAddFormTest(TestCase):
    # Test title fields
    def test_article_add_form_title_field(self):
        form = ArticleAddForm()
        self.assertTrue(form.fields['title'].label == None or form.fields['title'].label == 'Title')

    def test_article_add_form_title_max_length_field(self):
        form = ArticleAddForm()
        self.assertTrue(form.fields['title'].widget.attrs['maxlength'], 60)

    def test_article_add_form_title_min_length_field(self):
        form = ArticleAddForm()
        self.assertTrue(form.fields['title'].widget.attrs['minlength'], 3)

    def test_article_add_form_title_valid(self):
        form = ArticleAddForm()
        form_widget_attrs = {'class': 'form-control', 'name': 'Input title here...'}
        form.fields['title'].widget.attrs = form_widget_attrs
        self.assertFalse(form.is_valid())
