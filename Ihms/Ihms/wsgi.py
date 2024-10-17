"""
WSGI config for Ihms project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from serverless_wsgi import handle_request
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now you can access your environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ihms.settings')  # Ensure this matches your project name

application = get_wsgi_application()

def handler(event, context):
    return handle_request(application, event, context)

