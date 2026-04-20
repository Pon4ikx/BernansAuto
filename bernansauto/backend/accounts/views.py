from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.core import signing
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import RegisterSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def _send_verification_email(self, user):
        signer = signing.TimestampSigner(salt='accounts.email_verification')
        token = signer.sign(str(user.id))
        verify_url = f"{settings.FRONTEND_BASE_URL.rstrip('/')}/verify-email?token={token}"

        send_mail(
            subject='Подтверждение email для Bernans Auto',
            message=(
                f'Здравствуйте, {user.username}!\n\n'
                f'Чтобы завершить регистрацию, подтвердите email по ссылке:\n{verify_url}\n\n'
                'Если вы не регистрировались на Bernans Auto, просто проигнорируйте это письмо.'
            ),
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        try:
            self._send_verification_email(user)
        except Exception:
            user.delete()
            return Response(
                {'detail': 'Не удалось отправить письмо подтверждения. Попробуйте позже.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            {'detail': 'Письмо с подтверждением отправлено на email.'},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        login_value = (request.data.get('login') or '').strip()
        password = request.data.get('password') or ''

        if not login_value or not password:
            return Response(
                {"detail": "Введите логин/email и пароль."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_obj = User.objects.filter(email__iexact=login_value).first()
        if user_obj and not user_obj.is_active:
            return Response(
                {"detail": "Подтвердите email перед входом в аккаунт."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_by_username = User.objects.filter(username=login_value).first()
        if user_by_username and not user_by_username.is_active:
            return Response(
                {"detail": "Подтвердите email перед входом в аккаунт."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = user_obj.username if user_obj else login_value
        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({"detail": "Неверный логин или пароль."}, status=status.HTTP_400_BAD_REQUEST)

        django_login(request, user)
        return Response(UserSerializer(user).data)


class LogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        django_logout(request)
        return Response({"detail": "Вы вышли из аккаунта."})


class MeView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Не авторизован."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(UserSerializer(request.user).data)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        token = (request.data.get('token') or '').strip()
        if not token:
            return Response({"detail": "Токен подтверждения не передан."}, status=status.HTTP_400_BAD_REQUEST)

        signer = signing.TimestampSigner(salt='accounts.email_verification')
        try:
            user_id = signer.unsign(token, max_age=60 * 60 * 24)
        except signing.SignatureExpired:
            return Response({"detail": "Ссылка подтверждения истекла."}, status=status.HTTP_400_BAD_REQUEST)
        except signing.BadSignature:
            return Response({"detail": "Некорректная ссылка подтверждения."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"detail": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

        if user.is_active:
            return Response({"detail": "Email уже подтвержден."}, status=status.HTTP_200_OK)

        user.is_active = True
        user.save(update_fields=['is_active'])
        return Response({"detail": "Email успешно подтвержден. Теперь вы можете войти."}, status=status.HTTP_200_OK)
