from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import *
from .models import MyUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.conf import settings
from django.core.mail import send_mail
import random
from rest_framework.permissions import BasePermission


def generate_random_integers() -> str:
    """
    Generates a random 6-digit integer.

    Returns:
        str: A string representing a random 6-digit integer.
    """
    random_integers = "".join(str(random.randint(1, 9)) for _ in range(6))
    return random_integers


@api_view(["POST"])
def register_user(request):
    if request.method == "POST":
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                token_serializer = CustomTokenObtainPairSerializer(data=request.data)
                token = token_serializer.get_token(user=user)
                return Response(
                    {
                        "refresh": str(token),
                        "access": str(token.access_token),
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(["POST"])
def login_user(request):
    if request.method == "POST":
        try:
            serializer = CustomTokenObtainPairSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.user
                token = serializer.get_token(user=user)
                return Response(
                    {
                        "refresh": str(token),
                        "access": str(token.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "Invalid credentials"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(["GET", "DELETE"])
@permission_classes([IsAdminUser])
def get_all_users_info(request):
    if request.method == "GET":
        try:
            users = MyUser.objects.all()
            serializer = UserSerializer(users, many=True)
            user_info = serializer.data
            user_info = [
                {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                    "admin": user["is_superuser"],
                    "created_date": user["created_date"],
                }
                for user in user_info
            ]
            return Response(user_info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    if request.method == "DELETE":
        try:
            MyUser.objects.all().delete()
            return Response(
                {"message": "All user accounts deleted"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(["GET"])
def detail_user_account(request, userid):
    try:
        user = MyUser.objects.get(id=userid)
    except MyUser.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        try:
            serializer = UserSerializer(user)
            user_info = serializer.data
            user_info["admin"] = user.is_superuser
            return Response(user_info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == "POST":
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")

            if not user.check_password(old_password):
                return Response(
                    {"detail": "Invalid old password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()

            return Response(
                {"detail": "Password updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------

# Resetting password views


@api_view(["POST"])
def request_otp(request):
    if request.method == "POST":
        email_address = request.data.get("email")

        if email_address:
            otp = generate_random_integers()
            try:
                user = MyUser.objects.get(email=email_address)
                user.otp_code = otp
                user.save()
            except MyUser.DoesNotExist:
                return Response(
                    {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

            subject = "Password Reset OTP"
            message = f"Your OTP for password reset is: {otp}"
            from_email = settings.EMAIL_HOST_USER
            to_email = [email_address]

            send_mail(subject, message, from_email, to_email, fail_silently=False)

            return Response({"message": "OTP sent successfully"})
        else:
            return Response(
                {"error": "Email address is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["POST"])
def enter_otp(request):
    if request.method == "POST":
        email_address = request.data.get("email")
        otp_entered = request.data.get("otp")

        if email_address and otp_entered:
            try:
                user = MyUser.objects.get(email=email_address, otp_code=otp_entered)
                return Response(
                    {"message": "OTP verification successful", "email": email_address}
                )
            except MyUser.DoesNotExist:
                return Response(
                    {"message": "Invalid email or OTP code"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Email address and OTP are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["POST"])
def reset_password(request):
    if request.method == "POST":
        email_address = request.data.get("email")
        new_password = request.data.get("new_password")

        if email_address and new_password:
            try:
                user = MyUser.objects.get(email=email_address)
                user.set_password(new_password)
                user.otp_code = None
                user.save()
                return Response({"message": "Password reset successfully"})
            except MyUser.DoesNotExist:
                return Response(
                    {"message": "Invalid email or OTP code"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Email address and new password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# -----------
