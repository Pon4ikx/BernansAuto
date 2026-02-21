from rest_framework import serializers
from .models import Car, Motorcycle, Car_Photo, Moto_Photo, Favorite


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class Car_PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car_Photo
        fields = "__all__"


class MotorcycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorcycle
        fields = "__all__"


class Moto_PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moto_Photo
        fields = "__all__"


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"
