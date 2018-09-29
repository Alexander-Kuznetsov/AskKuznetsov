import datetime

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from ask_kuznetsov.models import Profile, Question, Answer, Tag


class SearchForm(forms.Form):
    search_word = forms.CharField(
        min_length=2,
        max_length=20,
        label="Search",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search'
        })
    )


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
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Input tags here...'
        })
    )

    def __init__(self, user=None, *args, **kwargs):
        self._user = user
        forms.Form.__init__(self, *args, **kwargs)

    def clean_tags(self):
        tags_list = self.cleaned_data.get('tags', '').split(',')
        if tags_list:
            for sym in ['\\', ']', '[', '%']:
                for tag in tags_list:
                    if tag.find(sym) != -1:
                        raise forms.ValidationError(u'Error symbol in tag')
        return tags_list

    def save(self, user):
        article = Question()
        article.title = self.cleaned_data['title']
        article.text = self.cleaned_data['text']

        tags_list = self.cleaned_data['tags']
        if tags_list:
            tags_list = [tag.replace(' ', '') for tag in tags_list]
            tags_list = [tag.replace('-', '_') for tag in tags_list]

        article.created_at = datetime.datetime.now()
        article.rating_like = 0
        article.rating_dislike = 0
        article.author = user
        article.save()

        for tag in tags_list:
            tag_obj = Tag.objects.get_or_create(tag)
            article.tags.add(tag_obj)

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

    def save(self, article, user):
        answer = Answer()
        answer.text = self.cleaned_data['text']
        answer.created_at = datetime.datetime.now()
        answer.rating_like = 0
        answer.rating_dislike = 0
        answer.author = user
        answer.question = article
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


class SettingsForm(forms.Form):
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
    password = forms.CharField(
        min_length=4,
        max_length=20,
        label='Password:',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '***********'
        })
    )

    def __init__(self, user=None, *args, **kwargs):
        self._user = user
        forms.Form.__init__(self, *args, **kwargs)

    def save(self, user):
        user.login = self.cleaned_data['login']
        user.email = self.cleaned_data['email']
        user.password = self.cleaned_data['password']
        user.save()

        return user
