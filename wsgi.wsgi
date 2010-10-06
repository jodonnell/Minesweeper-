import os, sys

sys.path.append('/home/jodonnell/games/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp/eggs'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
