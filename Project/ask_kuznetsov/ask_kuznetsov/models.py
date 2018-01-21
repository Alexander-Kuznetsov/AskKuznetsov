from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

GOOD_RATING = 2

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
		return self.filter(rating__gt=GOOD_RATING).order_by('-rating')

	def new_questions(self):
		return self.order_by('-created_at')


class Question(models.Model):
	title = models.CharField(max_length=60)
	text = models.TextField()
	author = models.ForeignKey(Profile)
	rating = models.IntegerField(default=0)
	created_at = models.DateTimeField(default=timezone.now)
	tags = models.ManyToManyField('Tag')
	
	objects = QuestionManager()

	def nice_title(self):
		return self.title + '?'

	def get_url(self):
		return '/question{question_id}/'.format(question_id=self.id)

	def get_answers(self):
	   	return Answer.objects.filter(answer_question_id=self.id)

	def __unicode__(self):
		return u'{0} - {1}'.format(self.id, self.title)


class Answer(models.Model):
	text = models.TextField()
	author = models.ForeignKey(Profile)
	created_at = models.DateTimeField(default=timezone.now)
	question = models.ForeignKey(Question)
	rating = models.IntegerField(default=0)
	
	#objects = AnswerManager()

	def get_url(self):
        return self.question.get_url()

	def __unicode__(self):
		return u'{0} - {1}'.format(self.id, self.text)


class Tag(models.Model):
	name = models.CharField(max_length=60)