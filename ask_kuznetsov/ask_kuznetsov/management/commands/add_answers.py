from django.core.management.base import BaseCommand, CommandError
from Project.models import Profile, Question, Answer
from random import choice

class Command(BaseCommand):
  help = 'creates fake answers'

  def add_arguments(self, parser):
    parser.add_argument('-n', action = 'store', dest = 'count', default = 10, help = 'number of users to add')

  def handle(self, *args, **options):
    count = int(options['count'])
    users = Profile.objects.all()[1:]
    question = Question.objects.all()[1:]
    for i in range(0, count):
      answer = Answer()
      answer.question = choice(question)
      answer.text = 'Answer_text' + str(answer.question.id) + '_' + str(answer.id)
      answer.author = choice(users)
      answer.save()