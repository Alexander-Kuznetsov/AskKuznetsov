from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Sum, F
from django.core.urlresolvers import reverse
from django.db.models.functions import Coalesce
import datetime

GOOD_RATING = 10


class Profile(models.Model):
	avatar = models.ImageField(upload_to="avatars/")
	user = models.OneToOneField(User)

	def avatar_url(self):
		if self.avatar and hasattr(self.avatar, 'url'):
			return self.avatar.url
		else:
			return os.path.join(settings.MEDIA_URL, 'avatars', 'avatar.jpg')


class QuestionManager(models.Manager):
	def best_questions(self):
		return self.annotate(count=F('rating_like') - F('rating_dislike')).filter(count__gt=GOOD_RATING).order_by("-count")

	def new_questions(self):
		return self.order_by('-created_at')


class TagManager(models.Manager):
	def get_or_create(self, title):
		print(title)
		try:
			tag = self.get_by_title(title)
		except:
			print('##################################################')
			print(title)
			print('##################################################')
			tag = self.create(title=title)
		return tag

	# searches using title
	def get_by_title(self, title):
		print(self.get(title=title))
		return self.get(title=title)


class Tag(models.Model):
	title = models.CharField(max_length=100)

	def get_url(self):
		return reverse(kwargs={'tag': self.title})

	objects = TagManager()


class QuestionManager(models.Manager):
    qs = None

    def init(self):
        self.qs = self.get_queryset()
        return self

    def get_query(self):
        return self.qs

    def add_tags(self):
        self.qs.prefetch_related('tags')
        return self


class Question(models.Model):
	title = models.CharField(max_length=60)
	text = models.TextField()
	author = models.ForeignKey(Profile)
	rating_like = models.IntegerField(default=0)
	rating_dislike = models.IntegerField(default=0)
	created_at = models.DateTimeField(default=timezone.now)
	tags = models.ManyToManyField(Tag)
	objects = QuestionManager()

	def nice_title(self):
		return self.title + '?'

	def get_url(self):
		return '/question{question_id}/'.format(question_id=self.id)

	def get_answers(self):
		return Answer.objects.filter(answer_question_id=self.id)

	def __unicode__(self):
		return u'{0} - {1}'.format(self.id, self.title)

	def get_count_answers(self):
		return Answer.objects.filter(question_id=self.id).count()

	def get_rating(self):
		return self.rating_like - self.rating_dislike



class Answer(models.Model):
	text = models.TextField()
	author = models.ForeignKey(Profile)
	created_at = models.DateTimeField(default=timezone.now)
	question = models.ForeignKey(Question)
	rating_like = models.IntegerField(default=0)
	rating_dislike = models.IntegerField(default=0)

	def get_url(self):
		return self.question.get_url()

	def __unicode__(self):
		return u'{0} - {1}'.format(self.id, self.text)


class LikesQuestion(models.Model):
	rating_like = models.IntegerField(default=0)
	rating_dislike = models.IntegerField(default=0)
	question = models.ForeignKey(Question)
	author = models.ForeignKey(Profile)

	def get_rating(self):
		pass



class LikesAnswer(models.Model):
	rating_like = models.IntegerField(default=0)
	rating_dislike = models.IntegerField(default=0)
	question = models.ForeignKey(Question)
	answer = models.ForeignKey(Answer)
	author = models.ForeignKey(Profile)