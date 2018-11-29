from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User

from ask_project.models import Profile, Question, Answer, Tag

class Command(BaseCommand):
  def handle(self, *args, **options):
        users = User.objects.all()
        users.delete()
        profile = Profile.objects.all()
        profile.delete()
        tags = Tag.objects.all()
        tags.delete()
        questions = Question.objects.all()
        questions.delete()
        answers = Answer.objects.all()
        answers.delete()
