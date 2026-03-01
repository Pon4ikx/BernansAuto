from rest_framework import viewsets
from .models import Car, Motorcycle, Car_Photo, Moto_Photo, CarFavorite, MotoFavorite
from .serializers import (
    CarSerializer,
    MotorcycleSerializer,
    Car_PhotoSerializer,
    Moto_PhotoSerializer,
    CarFavoriteSerializer,
    MotoFavoriteSerializer,
)


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = "slug"


class MotorcycleViewSet(viewsets.ModelViewSet):
    queryset = Motorcycle.objects.all()
    serializer_class = MotorcycleSerializer
    lookup_field = "slug"


class Car_PhotoViewSet(viewsets.ModelViewSet):
    queryset = Car_Photo.objects.all()
    serializer_class = Car_PhotoSerializer


class Moto_PhotoViewSet(viewsets.ModelViewSet):
    queryset = Moto_Photo.objects.all()
    serializer_class = Moto_PhotoSerializer


class CarFavoriteViewSet(viewsets.ModelViewSet):
    queryset = CarFavorite.objects.all()
    serializer_class = CarFavoriteSerializer


class MotoFavoriteViewSet(viewsets.ModelViewSet):
    queryset = MotoFavorite.objects.all()
    serializer_class = MotoFavoriteSerializer
