from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ask_project.models import Profile

from django.core.files import File
from random import choice

username = '2freeWwjd 4meYourGirl Airtiumen Allycenton Amorphon Anicware Aracrossent Asonican Auxillwor'
'Bootypersto BugsAware Chilotes Chonexpiryi ChooseNeat Citadmarl Comgewo DarkSlipk DasMidnight'
'Delivivi Discoverda DoggXcaptain DravenHemp Dressyhose Ephornet Esollaur Exterstp Extrammun'
'Feodata Figgird'

username = username.split(' ')

class Command(BaseCommand):
  help = 'creates fake users'

  def add_arguments(self, parser):
    parser.add_argument('-n', action = 'store', dest = 'count', default = 10, help = 'number of users to add')

  def handle(self, *args, **options):
    count = int(options['count'])
    for i in range(0, count):
      user = User()
      user.save()

      user.username = choice(username) + str(user.id)
      print(user.username)
      user.first_name = choice(username) + str(user.id)
      user.last_name = choice(username) + str(user.id)
      user.email = choice(username) + str(user.id) + '@mail.ru'
      user.password = make_password('Imabot')
      user.is_active = True
      user.is_superuser = False
      user.save()

      user_data = Profile()
      user_data.user = user

      user_data.save()

#self.stdout.write('[%d] added user %s' % (user.id, user.username))
