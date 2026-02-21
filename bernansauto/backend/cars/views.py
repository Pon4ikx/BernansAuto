from rest_framework import viewsets
from .models import Car, Motorcycle, Car_Photo, Moto_Photo, Favorite
from .serializers import (
    CarSerializer,
    MotorcycleSerializer,
    Car_PhotoSerializer,
    Moto_PhotoSerializer,
    FavoriteSerializer,
)


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class MotorcycleViewSet(viewsets.ModelViewSet):
    queryset = Motorcycle.objects.all()
    serializer_class = MotorcycleSerializer


class Car_PhotoViewSet(viewsets.ModelViewSet):
    queryset = Car_Photo.objects.all()
    serializer_class = Car_PhotoSerializer


class Moto_PhotoViewSet(viewsets.ModelViewSet):
    queryset = Moto_Photo.objects.all()
    serializer_class = Moto_PhotoSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
