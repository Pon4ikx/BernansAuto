from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Car, Motorcycle, Car_Photo, Moto_Photo, CarFavorite, MotoFavorite
from .serializers import (
    CarSerializer,
  PopularCarSerializer,
    MotorcycleSerializer,
  PopularMotorcycleSerializer,
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
    serializer_class = CarFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CarFavorite.objects.filter(user=self.request.user).select_related("car")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MotoFavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = MotoFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MotoFavorite.objects.filter(user=self.request.user).select_related("motorcycle")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CarFavoriteToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        car_id = request.data.get("car_id")
        if not car_id:
            return Response({"detail": "car_id обязателен."}, status=status.HTTP_400_BAD_REQUEST)

        car = Car.objects.filter(id=car_id).first()
        if not car:
            return Response({"detail": "Автомобиль не найден."}, status=status.HTTP_404_NOT_FOUND)

        favorite = CarFavorite.objects.filter(user=request.user, car=car).first()
        if favorite:
            favorite.delete()
            return Response({"is_favorite": False}, status=status.HTTP_200_OK)

        CarFavorite.objects.create(user=request.user, car=car)
        return Response({"is_favorite": True}, status=status.HTTP_200_OK)


class MotoFavoriteToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        motorcycle_id = request.data.get("motorcycle_id")
        if not motorcycle_id:
            return Response({"detail": "motorcycle_id обязателен."}, status=status.HTTP_400_BAD_REQUEST)

        motorcycle = Motorcycle.objects.filter(id=motorcycle_id).first()
        if not motorcycle:
            return Response({"detail": "Мототехника не найдена."}, status=status.HTTP_404_NOT_FOUND)

        favorite = MotoFavorite.objects.filter(user=request.user, motorcycle=motorcycle).first()
        if favorite:
            favorite.delete()
            return Response({"is_favorite": False}, status=status.HTTP_200_OK)

        MotoFavorite.objects.create(user=request.user, motorcycle=motorcycle)
        return Response({"is_favorite": True}, status=status.HTTP_200_OK)


class PopularCarsView(APIView):
    def get(self, request):
        qs = (
            Car.objects.filter(available=True)
            .annotate(favorite_count=Count("car_favorites"))
            .order_by("-favorite_count", "-created_at")
        )
        top = qs[:3]
        return Response(PopularCarSerializer(top, many=True).data)


class PopularMotorcyclesView(APIView):
    def get(self, request):
        qs = (
            Motorcycle.objects.filter(available=True)
            .annotate(favorite_count=Count("moto_favorites"))
            .order_by("-favorite_count", "-created_at")
        )
        top = qs[:3]
        return Response(PopularMotorcycleSerializer(top, many=True).data)
