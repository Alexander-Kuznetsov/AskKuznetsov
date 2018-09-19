import datetime

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from ask_kuznetsov.models import Profile, Question, Answer, Tag


class ArticleAddForm(forms.Form):
    title = forms.CharField(
        min_length=3,
        max_length=60,
        label='Title',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Input title here...'
        })

    )
    text = forms.CharField(
        min_length=3,
        max_length=1000,
        label='Text',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Input text here...',
            'rows': '10'
        })
    )
    tags = forms.CharField(
        label='Tags',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Input tags here...'
        })
    )

    def __init__(self, user=None, *args, **kwargs):
        self._user = user
        forms.Form.__init__(self, *args, **kwargs)

    def save(self):
        article = Question()
        article.title = self.cleaned_data['title']
        article.text = self.cleaned_data['text']
        article.created_at = datetime.datetime.now()
        article.rating_like = 0
        article.rating_dislike = 0
        article.author = Profile.objects.all()[1]
        article.save()

        return article


class AnswerAddForm(forms.Form):
    text = forms.CharField(
        min_length=3,
        max_length=255,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Input text here...',
            'rows': '6'
        })
    )

    def __init__(self, user=None, *args, **kwargs):
        self._user = user
        forms.Form.__init__(self, *args, **kwargs)

    def save(self):
        answer = Answer()
        answer.text = self.cleaned_data['text']
        answer.created_at = datetime.datetime.now()
        answer.rating_like = 0
        answer.rating_dislike = 0
        answer.author = Profile.objects.all()[1]
        answer.question = Question.objects.all()[1]
        answer.save()

        return answer


class RegistrationForm(forms.Form):
    login = forms.CharField(
        min_length=3,
        max_length=20,
        label='Login:',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'SuperPupkin'
        })
    )

    email = forms.CharField(
        min_length=3,
        max_length=255,
        label='Email:',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'pupkin@mail.ru'
        })
    )
    name = forms.CharField(
        min_length=3,
        max_length=20,
        label='Name:',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pupkin'
        })
    )
    password = forms.CharField(
        min_length=4,
        max_length=20,
        label='Password:',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '***********'
        })
    )
    password_repeat = forms.CharField(
        min_length=4,
        max_length=20,
        label='Repeat password:',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '***********'
        })
    )

    def clean_password_repeat(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_repeat']:
            raise forms.ValidationError('Passwords are not equal.')

    def save(self):
        user = User.objects.create_user(self.cleaned_data['login'], self.cleaned_data['email'],
                                        self.cleaned_data['password'])

        Profile.objects.create(user=user)


class SignInForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    _user = None

    def clean(self):
        try:
            self._user = auth.authenticate(username=self.cleaned_data['username'],
                                           password=self.cleaned_data['password'])
        except:
            raise forms.ValidationError('Invalid login or password')

    def auth(self):
        if not self._user:
            self.clean()
        return self._user
