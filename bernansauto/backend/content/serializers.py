from rest_framework import serializers

from .models import Contact, News


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'address', 'phone', 'email', 'work_hours', 'map_link')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'text', 'photo', 'published_at')

