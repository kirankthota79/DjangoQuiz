"""
WSGI config for quiz project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import django 
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PyQuiz.settings')
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PyQuiz.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
application = get_wsgi_application()
django.setup()

# import django 
# django.setup()