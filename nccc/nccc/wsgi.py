"""
WSGI config for nccc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""



'''
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nccc.settings")

application = get_wsgi_application()
'''

#'''
import os, sys
from django.core.wsgi import get_wsgi_application
sys.path.append('/var/www/html/nccc')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nccc.settings'
application = get_wsgi_application()
#'''
#os.environ['HTTPS'] = "on"