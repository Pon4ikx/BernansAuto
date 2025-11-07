from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car                   # ← связываем с моделью
        fields = '__all__'             # ← сериализуем все поля модели
