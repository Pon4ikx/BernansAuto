from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet

router = DefaultRouter() # генерирует все стандартные CRUD-маршруты (list, create, retrieve, update, delete);
router.register(r'', CarViewSet)

urlpatterns = router.urls
