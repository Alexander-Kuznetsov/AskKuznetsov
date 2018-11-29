from django.core.management.base import BaseCommand, CommandError

from ask_project.models import Tag


class Command(BaseCommand):
  help = 'creates tags'

  def add_arguments(self, parser):
    parser.add_argument('-n', action = 'store', dest = 'count', default = 10, help = 'number of users to add')

  def handle(self, *args, **options):
    count = int(options['count'])
    for i in range(0, count):

      tag = Tag()
      tag.save()
      tag.name = 'Faketag_' + str(i % 23)
      tag.save()
