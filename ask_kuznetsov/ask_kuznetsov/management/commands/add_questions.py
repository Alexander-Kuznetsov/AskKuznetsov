from django.core.management.base import BaseCommand, CommandError

from ask_kuznetsov.models import Profile, Question

from random import choice

class Command(BaseCommand):
  help = 'creates fake questions'

  def add_arguments(self, parser):
    parser.add_argument('-n', action = 'store', dest = 'count', default = 10, help = 'number of users to add')

  def handle(self, *args, **options):
    count = int(options['count'])
    users = Profile.objects.all()[1:]
    for i in range(0, count):
      question = Question()
      question.title = 'Question_' + str(question.id)
      question.text = 'Question_text' + str(question.id) + str(i % 19)
      question.author = choice(users)
      #question.tag_set.add(choice(tag))
      question.save()
