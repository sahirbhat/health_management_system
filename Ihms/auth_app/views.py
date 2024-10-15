import boto3
import os
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Load environment variables from .env file
load_dotenv()

# Get AWS credentials and Cognito details from environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')

# Initialize the boto3 client for Cognito
cognito_client = boto3.client(
    'cognito-idp',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='ap-south-1'  # Change this to your AWS region
)

# Sign-Up API View
class SignUpView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')  # Get the name from request data

        try:
            response = cognito_client.sign_up(
                ClientId=os.getenv('COGNITO_CLIENT_ID'),
                Username=email,
                Password=password,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email
                    },
                    {
                        'Name': 'name',  # Add the name attribute
                        'Value': name
                    }
                ]
            )
            return Response({'message': 'User signed up successfully!'}, status=status.HTTP_201_CREATED)
        except cognito_client.exceptions.UsernameExistsException:
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
# Confirm User API View
class ConfirmUserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        confirmation_code = request.data.get('confirmation_code')

        try:
            response = cognito_client.confirm_sign_up(
                ClientId=COGNITO_CLIENT_ID,
                Username=email,
                ConfirmationCode=confirmation_code
            )
            return Response({'message': 'User confirmed successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Login API View
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            response = cognito_client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                },
                ClientId=COGNITO_CLIENT_ID
            )
            return Response(response['AuthenticationResult'], status=status.HTTP_200_OK)
        except cognito_client.exceptions.NotAuthorizedException:
            return Response({'error': 'Incorrect email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        except cognito_client.exceptions.UserNotConfirmedException:
            return Response({'error': 'User not confirmed'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
