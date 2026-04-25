from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.core import signing
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import AccountSettingsSerializer, RegisterSerializer, UserSerializer


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

        html = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.55; color: #20383f;">
          <h2 style="margin: 0 0 12px; color: #1995AD;">Подтверждение email</h2>
          <p style="margin: 0 0 10px;">Здравствуйте, <strong>{user.username}</strong>!</p>
          <p style="margin: 0 0 14px;">
            Чтобы завершить регистрацию, перейдите по <a href="{verify_url}" style="color: #1995AD; font-weight: 700;">ссылке</a>.
          </p>
          <div style="margin: 18px 0 10px;">
            <a href="{verify_url}" style="display: inline-block; background: #1995AD; color: #fff; text-decoration: none; padding: 10px 16px; border-radius: 8px; font-weight: 700;">
              Подтвердить email
            </a>
          </div>
          <p style="margin: 14px 0 0; color: #66777c; font-size: 12px;">
            Если вы не регистрировались на Bernans Auto — просто проигнорируйте это письмо.
          </p>
        </div>
        """

        send_mail(
            subject='Подтверждение email для Bernans Auto',
            message=(
                f'Здравствуйте, {user.username}!\n\n'
                f'Чтобы завершить регистрацию, подтвердите email по ссылке.\n\n'
                f'{verify_url}\n\n'
                'Если вы не регистрировались на Bernans Auto, просто проигнорируйте это письмо.'
            ),
            from_email=None,
            recipient_list=[user.email],
            html_message=html,
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
    def _get_authenticated_user(self, request):
        if not request.user.is_authenticated:
            return None
        return request.user

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        user = self._get_authenticated_user(request)
        if not user:
            return Response({"detail": "Не авторизован."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(UserSerializer(user).data)

    def patch(self, request):
        user = self._get_authenticated_user(request)
        if not user:
            return Response({"detail": "Не авторизован."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = AccountSettingsSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(user).data)

    def delete(self, request):
        user = self._get_authenticated_user(request)
        if not user:
            return Response({"detail": "Не авторизован."}, status=status.HTTP_401_UNAUTHORIZED)

        django_logout(request)
        user.delete()
        return Response({"detail": "Аккаунт удален."}, status=status.HTTP_200_OK)


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


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = (request.data.get('email') or '').strip().lower()
        if not email:
            return Response({"detail": "Введите email."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return Response({"detail": "Пользователь с таким email не найден."}, status=status.HTTP_404_NOT_FOUND)

        signer = signing.TimestampSigner(salt='accounts.password_reset')
        token = signer.sign(str(user.id))
        reset_url = f"{settings.FRONTEND_BASE_URL.rstrip('/')}/reset-password?token={token}"

        html = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.55; color: #20383f;">
          <h2 style="margin: 0 0 12px; color: #1995AD;">Сброс пароля</h2>
          <p style="margin: 0 0 10px;">Здравствуйте, <strong>{user.username}</strong>!</p>
          <p style="margin: 0 0 14px;">
            Чтобы сбросить пароль, перейдите по <a href="{reset_url}" style="color: #1995AD; font-weight: 700;">ссылке</a>.
          </p>
          <div style="margin: 18px 0 10px;">
            <a href="{reset_url}" style="display: inline-block; background: #1995AD; color: #fff; text-decoration: none; padding: 10px 16px; border-radius: 8px; font-weight: 700;">
              Сбросить пароль
            </a>
          </div>
          <p style="margin: 14px 0 0; color: #66777c; font-size: 12px;">
            Если вы не запрашивали сброс пароля — просто проигнорируйте это письмо.
          </p>
        </div>
        """

        try:
            send_mail(
                subject='Сброс пароля Bernans Auto',
                message=(
                    f'Здравствуйте, {user.username}!\n\n'
                    f'Чтобы сбросить пароль, перейдите по ссылке.\n\n'
                    f'{reset_url}\n\n'
                    'Если вы не запрашивали сброс пароля — просто проигнорируйте это письмо.'
                ),
                from_email=None,
                recipient_list=[user.email],
                html_message=html,
                fail_silently=False,
            )
        except Exception:
            return Response(
                {"detail": "Не удалось отправить письмо. Проверьте настройки почты и попробуйте позже."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({"detail": "Мы отправили письмо со ссылкой для сброса пароля."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        token = (request.data.get('token') or '').strip()
        new_password = request.data.get('new_password') or ''
        confirm_new_password = request.data.get('confirm_new_password') or ''

        if not token:
            return Response({"detail": "Токен не передан."}, status=status.HTTP_400_BAD_REQUEST)
        if not new_password or not confirm_new_password:
            return Response({"detail": "Введите новый пароль и подтверждение."}, status=status.HTTP_400_BAD_REQUEST)
        if new_password != confirm_new_password:
            return Response({"detail": "Пароли не совпадают."}, status=status.HTTP_400_BAD_REQUEST)

        signer = signing.TimestampSigner(salt='accounts.password_reset')
        try:
            user_id = signer.unsign(token, max_age=60 * 60)  # 1 час
        except signing.SignatureExpired:
            return Response({"detail": "Ссылка сброса пароля истекла."}, status=status.HTTP_400_BAD_REQUEST)
        except signing.BadSignature:
            return Response({"detail": "Некорректная ссылка сброса пароля."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"detail": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

        # те же правила, что при регистрации (минимум 8, 1 строчная, 1 заглавная)
        import re
        if len(new_password) < 8:
            return Response({"detail": "Пароль должен быть не короче 8 символов."}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search(r'[a-z]', new_password):
            return Response({"detail": "Пароль должен содержать хотя бы одну строчную букву."}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search(r'[A-Z]', new_password):
            return Response({"detail": "Пароль должен содержать хотя бы одну заглавную букву."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save(update_fields=['password'])
        return Response({"detail": "Пароль обновлен. Теперь вы можете войти."}, status=status.HTTP_200_OK)
