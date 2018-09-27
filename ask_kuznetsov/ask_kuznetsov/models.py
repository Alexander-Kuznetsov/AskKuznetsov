from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Sum, F
from django.core.urlresolvers import reverse
from django.db.models.functions import Coalesce
import datetime
from django import template

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation

register = template.Library()

GOOD_RATING = 1


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

	def hot_questions(self):
		likes = LikeDislike.objects\
			.likes().values('object_id')\
			.annotate(count=Count('object_id'))\
			.filter(count__gte=GOOD_RATING)\
			.order_by('-count')
		ids = [like['object_id'] for like in likes]
		return self.all().filter(id__in=ids)

	def search_word(self, word):
		try:
			#return self.get(title__icontains=word)
			return self.filter(title=word)#.load_all()
		except:
			return None


class TagManager(models.Manager):
	def get_or_create(self, title):
		print(title)
		try:
			tag = self.get_by_title(title)
		except:
			#print('##################################################')
			#print(title)
			#print('##################################################')
			tag = self.create(title=title)
		return tag

	# searches using title
	def get_by_title(self, title):
		#print(self.get(title=title))
		return self.get(title=title)

	def get_count_iniq(self):
		return self.values(
			'title'
		).annotate(
			name_count=Count('title')
		).order_by("-name_count")[:8]


class Tag(models.Model):
	title = models.CharField(max_length=100)

	def get_url(self):
		return reverse(kwargs={'tag': self.title})

	objects = TagManager()

'''
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
'''

class LikeDislikeManager(models.Manager):
	use_for_related_fields = True

	def likes(self):
		return self.get_queryset().filter(vote__gt=0)

	def dislikes(self):
		return self.get_queryset().filter(vote__lt=0)

	def sum_rating(self):
		return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

	def question(self):
		return self.get_queryset().filter(content_type__model='question').order_by('-articles__pub_date')

	def answer(self):
		return self.get_queryset().filter(content_type__model='answer').order_by('-comments__pub_date')

	def get_top_people(self):
		top_people = self.likes().values('user_id').annotate(count=Count('user_id')).order_by('-count')
		return [User.objects.get(id=top_man['user_id']) for top_man in top_people]


class LikeDislike(models.Model):
	LIKE = 1
	DISLIKE = -1

	VOTES = (
		(DISLIKE, 'dislike'),
		(LIKE, 'like')
	)

	vote = models.SmallIntegerField(verbose_name=("Vote"), choices=VOTES)
	user = models.ForeignKey(User, verbose_name=("Author"))

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()

	objects = LikeDislikeManager()


class Question(models.Model):
	title = models.CharField(max_length=60)
	text = models.TextField()
	author = models.ForeignKey(Profile)
	rating_like = models.IntegerField(default=0)
	rating_dislike = models.IntegerField(default=0)
	created_at = models.DateTimeField(default=timezone.now)
	votes = GenericRelation(LikeDislike, related_query_name='question')
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

	def get_count_likes(self):
		return LikeDislike.objects.likes().values('object_id').filter(object_id=self.id).count()

	def get_count_dislikes(self):
		return LikeDislike.objects.dislikes().values('object_id').filter(object_id=self.id).count()


class Answer(models.Model):
	text = models.TextField()
	author = models.ForeignKey(Profile)
	created_at = models.DateTimeField(default=timezone.now)
	question = models.ForeignKey(Question)
	rating_like = models.IntegerField(default=0)
	rating_dislike = models.IntegerField(default=0)
	votes = GenericRelation(LikeDislike, related_query_name='answer')

	def get_url(self):
		return self.question.get_url()

	def __unicode__(self):
		return u'{0} - {1}'.format(self.id, self.text)





'''
class LikeDislikeManager(models.Manager):
	def has_question(self, question):
		return self.filter(question=question)

	def sum_for_question(self, question):
		res = self.has_question(question).aggregate(sum=Sum('rating_like'))['sum']
		return res if res else 0

	def add_or_update(self, owner, question, value):
		obj, new = self.update_or_create(
			author=owner,
			question=question,
			defaults={'rating_like': value}
		)
		question.rating_like = self.sum_for_question(question)
		question.save()
		return new


class LikeDislike(models.Model):
	LIKE = 1
	DISLIKE = 1

	rating_like = models.IntegerField(default=0)
	rating_dislike = models.IntegerField(default=0)
	question = models.ForeignKey(Question)
	author = models.ForeignKey(Profile)

	object = LikeDislikeManager()
'''