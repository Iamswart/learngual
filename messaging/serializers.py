from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp', 'read']

class MessageReadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'read']

    def update(self, instance, validated_data):
        instance.read = validated_data.get('read', instance.read)
        instance.save()
        return instance
