from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import LoginView, LogoutView, MeView, RegisterView, UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('login/', LoginView.as_view(), name='accounts-login'),
    path('register/', RegisterView.as_view(), name='accounts-register'),
    path('logout/', LogoutView.as_view(), name='accounts-logout'),
    path('me/', MeView.as_view(), name='accounts-me'),
] + router.urls
