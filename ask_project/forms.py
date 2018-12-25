import datetime

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from ask_project.models import Profile, Question, Answer, Tag


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
        label='Login',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'SuperPupkin'
        })
    )

    email = forms.CharField(
        min_length=3,
        max_length=255,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'pupkin@mail.ru'
        })
    )
    name = forms.CharField(
        min_length=3,
        max_length=20,
        label='Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pupkin'
        })
    )
    password = forms.CharField(
        min_length=4,
        max_length=20,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '***********'
        })
    )
    password_repeat = forms.CharField(
        min_length=4,
        max_length=20,
        label='Repeat password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '***********'
        })
    )

    avatar = forms.FileField(
        label='Avatar',
        required=False
    )

    def clean_login(self):
        username = self.cleaned_data['login']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('User with this login exist!')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with this email exist!')
        return email

    def clean_password_repeat(self):
        password_repeat = self.cleaned_data['password_repeat']
        if self.cleaned_data['password'] != password_repeat:
            raise forms.ValidationError('Passwords are not equal.')
        return password_repeat

    '''
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if avatar is not None and 'avatar' not in avatar.content_type:
            raise forms.ValidationError(u'Format file is bad!')
        return avatar
    '''

    def clean(self):
        # Create user
        # If exist -> Exception
        pass

    def save(self):
        user = User.objects.create_user(self.cleaned_data['login'], self.cleaned_data['email'],
                                        self.cleaned_data['password'])
        if self.cleaned_data['avatar'] is None:
            print('WARNING -avatar is None')
            return Profile.objects.create(user=user)
        return Profile.objects.create(user=user, avatar=self.cleaned_data['avatar'])



class SignInForm(forms.Form):
    username = forms.CharField(
        label='Username',
        min_length=3,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        label='Password',
        min_length=4,
        max_length=20,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    error_messages = {
        'invalid_login': "Please enter a correct username and password. "
                           "Note that both fields are case-sensitive.",
        'inactive': "This account is inactive.",
    }

    _user = None

    def clean(self):
        email = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if email and password:
            self._user = auth.authenticate(username=email, password=password)
            if self._user is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login'
                )
            else:
                self.confirm_login_allowed(self._user)

        return self.cleaned_data


        #if not User.objects.filter(username=self.cleaned_data['username']).exists():
        #    raise forms.ValidationError('User with this login not exist!')

        #user = User.objects.get(username=self.cleaned_data['username'])
        #if user and not user.check_password(self.cleaned_data['password']):
        #    raise forms.ValidationError('Wrong password!')


    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self._user


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

    password = forms.CharField(
        min_length=4,
        max_length=20,
        label='Password:',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '***********'
        })
    )

    newPassword = forms.CharField(
        min_length=4,
        max_length=20,
        label='New Password:',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '***********'
        })
    )

    newPasswordRepeat = forms.CharField(
        min_length=4,
        max_length=20,
        label='Repeat Password:',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '***********'
        })
    )

    def __init__(self, user=None, *args, **kwargs):
        self._user = user
        forms.Form.__init__(self, *args, **kwargs)

    def save(self, user):
        #User.objects.update(login=self.cleaned_data['login'], email=self.cleaned_data['email'],
        #                         password=self.cleaned_data['password'])

        user.username = self.cleaned_data['login']
        user.set_password(self.cleaned_data['newPassword'])
        user.save()

        return user
