from django.core.management.base import BaseCommand, CommandError
from ask_kuznetsov.models import *
from random import choice

answer_text = [
  'Ill finish Thor and then I think Ill check out either La Grande Illusion or '
  'another episode of Breaking Bad. Depends on what time it is.',

  'I plan on finishing Jarmuschs Dead Man',

  'Merry Christmas Mr. Lawrence. Or I was, but then I started scoring the main theme on piano.',

  'That underwear is REALLY expensive in San Francisco',

  'The movie never really gives enough information which is one of the reasons '
  'I dont like it. I feel that the twist was too gimmicky',

  'I love Body Heat! The Last Seduction and Sea of Love are really good ones as well.',

  'Out of all those movies I guess my order would be Sea of Love, The Last Seduction, and then Body Heat.'
]

class Command(BaseCommand):
  help = 'creates fake answers'

  def add_arguments(self, parser):
    parser.add_argument('-n', action = 'store', dest = 'count', default = 10, help = 'number of users to add')

  def handle(self, *args, **options):
    count = int(options['count'])
    users = Profile.objects.all()[0:]
    question = Question.objects.all()[0:]
    for i in range(0, count):
      answer = Answer()
      answer.question = choice(question)
      answer.text = choice(answer_text)
      answer.author = choice(users)
      answer.save()

