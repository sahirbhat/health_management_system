# auth_app/cognito_auth.py

import os
import jwt
import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from dotenv import load_dotenv
from django.utils.translation import gettext as _  # For translation support

# Load environment variables from .env
load_dotenv()

class CognitoJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed({
                'message': _('Authentication credentials were not provided.'),
                'login_url': '/auth/login/',  # Replace with your actual login URL
                'register_url': '/auth/register/'  # Replace with your actual register URL
            })

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            raise AuthenticationFailed({
                'message': _('Invalid token header. No token provided.'),
                'login_url': '/auth/login/',
                'register_url': '/auth/register/'
            })

        try:
            # Fetch the public key for token verification
            jwks_url = f'https://cognito-idp.{os.getenv("AWS_REGION")}.amazonaws.com/{os.getenv("COGNITO_USER_POOL_ID")}/.well-known/jwks.json'
            response = requests.get(jwks_url)
            jwks = response.json()['keys']

            header = jwt.get_unverified_header(token)
            kid = header['kid']

            rsa_key = {}
            for key in jwks:
                if key['kid'] == kid:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }

            if not rsa_key:
                raise AuthenticationFailed({
                    'message': _('Public key not found.'),
                    'login_url': '/auth/login/',
                    'register_url': '/auth/register/'
                })

            decoded_token = jwt.decode(
                token,
                rsa_key,
                algorithms=['RS256'],
                audience=os.getenv('COGNITO_CLIENT_ID')
            )

            return (decoded_token, None)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({
                'message': _('Token has expired.'),
                'login_url': '/auth/login/',
                'register_url': '/auth/register/'
            })
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({
                'message': _('Invalid token.'),
                'login_url': '/auth/login/',
                'register_url': '/auth/register/'
            })
