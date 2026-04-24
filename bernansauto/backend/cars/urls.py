from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CarViewSet,
    MotorcycleViewSet,
    Car_PhotoViewSet,
    Moto_PhotoViewSet,
    CarFavoriteViewSet,
    MotoFavoriteViewSet,
    CarFavoriteToggleView,
    MotoFavoriteToggleView,
    PopularCarsView,
    PopularMotorcyclesView,
)

router = DefaultRouter()
router.register(r"motorcycles", MotorcycleViewSet, basename="motorcycle")
router.register(r"car-photos", Car_PhotoViewSet, basename="car_photo")
router.register(r"moto-photos", Moto_PhotoViewSet, basename="moto_photo")
router.register(r"car-favorites", CarFavoriteViewSet, basename="car_favorite")
router.register(r"moto-favorites", MotoFavoriteViewSet, basename="moto_favorite")
router.register(r"", CarViewSet, basename="car")

urlpatterns = router.urls
urlpatterns += [
    path("popular/cars/", PopularCarsView.as_view(), name="popular-cars"),
    path("popular/motorcycles/", PopularMotorcyclesView.as_view(), name="popular-motorcycles"),
    path("favorites/car/toggle/", CarFavoriteToggleView.as_view(), name="car-favorite-toggle"),
    path("favorites/moto/toggle/", MotoFavoriteToggleView.as_view(), name="moto-favorite-toggle"),
]
