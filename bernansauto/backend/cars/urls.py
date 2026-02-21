from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CarViewSet,
    MotorcycleViewSet,
    Car_PhotoViewSet,
    Moto_PhotoViewSet,
    FavoriteViewSet,
)

router = DefaultRouter()
router.register(r"motorcycles", MotorcycleViewSet, basename="motorcycle")
router.register(r"car-photos", Car_PhotoViewSet, basename="car_photo")
router.register(r"moto-photos", Moto_PhotoViewSet, basename="moto_photo")
router.register(r"favorites", FavoriteViewSet, basename="favorite")
router.register(r"", CarViewSet, basename="car")

urlpatterns = router.urls
