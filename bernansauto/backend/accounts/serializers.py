from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User                   # ← связываем с моделью
        fields = '__all__'             # ← сериализуем все поля модели
