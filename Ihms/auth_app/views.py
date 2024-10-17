import boto3
import os
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

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
    permission_classes = [AllowAny]
    """
    Handle user signup using AWS Cognito.
    """
    def post(self, request):
        # Extract email, password, and name from the request data
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')  # Get the name from the request

        # Validate input fields
        if not email or not password or not name:
            return Response({'error': 'Email, password, and name are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Sign up user in Cognito
            response = cognito_client.sign_up(
                ClientId=COGNITO_CLIENT_ID,
                Username=email,
                Password=password,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'name', 'Value': name}
                ]
            )
            return Response({'message': 'User signed up successfully!'}, status=status.HTTP_201_CREATED)

        except cognito_client.exceptions.UsernameExistsException:
            return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Confirm User API View
class ConfirmUserView(APIView):
    permission_classes= [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        confirmation_code = request.data.get('confirmation_code')

        # Validate input fields
        if not email or not confirmation_code:
            return Response({'error': 'Email and confirmation code are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cognito_client.confirm_sign_up(
                ClientId=COGNITO_CLIENT_ID,
                Username=email,
                ConfirmationCode=confirmation_code
            )
            return Response({'message': 'User confirmed successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Login API View
class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate input fields
        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

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

# Forgot Password View
class ForgotPasswordView(APIView):
    permission_classes=[AllowAny]
    """
    This view handles the 'Forgot Password' functionality.
    It sends the reset code to the user's email/phone.
    """
    def post(self, request):
        username = request.data.get('username')

        if not username:
            return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = cognito_client.forgot_password(
                ClientId=COGNITO_CLIENT_ID,
                Username=username
            )
            return Response({
                "message": "Password reset code sent.",
                "delivery_details": response['CodeDeliveryDetails']
            }, status=status.HTTP_200_OK)

        except cognito_client.exceptions.UserNotFoundException:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error initiating forgot password: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Confirm Password Reset View
class ConfirmPasswordResetView(APIView):
    permission_classes=AllowAny
    """
    This view handles the 'Confirm Password Reset' functionality.
    It validates the confirmation code and resets the password.
    """
    def post(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        new_password = request.data.get('new_password')

        # Validate input fields
        if not username or not confirmation_code or not new_password:
            return Response({"error": "Username, confirmation code, and new password are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            cognito_client.confirm_forgot_password(
                ClientId=COGNITO_CLIENT_ID,
                Username=username,
                ConfirmationCode=confirmation_code,
                Password=new_password
            )
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)

        except cognito_client.exceptions.CodeMismatchException:
            return Response({"error": "Invalid confirmation code."}, status=status.HTTP_400_BAD_REQUEST)
        except cognito_client.exceptions.ExpiredCodeException:
            return Response({"error": "The confirmation code has expired."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error confirming password reset: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
