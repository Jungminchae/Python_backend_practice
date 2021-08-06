import jwt
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import RegisgerSerializer, EmailVerificationSerializer
from .models import User
from .utils import Util


class RegisterView(GenericAPIView):

    serializer_class = RegisgerSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data["email"])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse("email-verification")
        abs_url = "http://" + current_site + relative_link + "?token=" + str(token)

        email_body = (
            f"Hi {user.username} User link below to verify your email \n {abs_url}"
        )

        data = {
            "email_body": email_body,
            "email_subject": "Verify your email",
            "to_email": user.email,
        }
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):

    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Description",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get("token")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"email": "Activated"}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as e:
            return Response(
                {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as e:
            return Response(
                {"error": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST
            )
