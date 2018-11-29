from django.core.management.base import BaseCommand, CommandError

from ask_project.models import Profile, Question, Tag
from random import randint
from random import choice

question_title = [
  'Movie Youre Watching Tonigh',

  'Rate The Last Movie You Saw',

  'Its hard for me to rate horror movies'
]

question_text = [
  'Hi guys! As usual, it has been awhile! And by awhile, I mean a month long silence. '
  'A couple of things have happened since my last post. Well, the big one is when my little '
  'friend called anxiety came to visit and decided to stay for a bit. And he is an exhausting guest. ',

  'My theory is that in the movie, Catherine killed her parents when she was younger, killed her counselor '
  'in college with an ice pick and did the same to Johnny Boz and Gus and that Beth killed Nielson and her ex '
  'husband with the .38 years prior. And that Beth and Catherine remained lovers since college and Beth gave Catherine',

  'Simple enough; what film do you plan on seeing tonight, and what are your expectations? Im watching The Eiger Sanction, '
  'and being a Clint fan Ill be good. I might check out Taxi Driver as well, if I have time, which '
  'I have veeerrrry high hopes for.'
]

tags_name = ['Technopark', 'mailru', 'django', 'linux', 'cinema', 'horror', 'films']


class Command(BaseCommand):
  help = 'creates fake questions'

  def add_arguments(self, parser):
    parser.add_argument('-n', action = 'store', dest = 'count', default = 10, help = 'number of users to add')

  def handle(self, *args, **options):
    count = int(options['count'])
    users = Profile.objects.all()[0:]
    for i in range(0, count):
      question = Question()
      question.title = choice(question_title)
      question.text = choice(question_text)
      question.author = choice(users)
      question.save()

      count_tags = randint(1, 3)
      for i in range(count_tags):
        tag_obj = Tag.objects.get_or_create(choice(tags_name))
        question.tags.add(tag_obj)




