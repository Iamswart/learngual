from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageReadStatusSerializer, MessageSerializer


class UpdateMessageReadStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        message_ids = request.data.get("ids", [])
        messages = Message.objects.filter(id__in=message_ids, recipient=request.user)

        if not messages:
            return Response(
                {
                    "detail": "No messages found or you're not authorized to update them."
                },
                status=404,
            )

        messages.update(read=True)

        return Response(
            {"success": f"Updated {messages.count()} messages to read."}, status=200
        )

    # def post(self, request, *args, **kwargs):
    #     message_id = request.data.get('id')
    #     message = get_object_or_404(Message, id=message_id, recipient=request.user)

    #     if message.recipient != request.user:
    #         return Response({"detail": "Not authorized to update this message's read status."}, status=403)

    #     serializer = MessageReadStatusSerializer(message, data={'read': True}, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"success": "Message read status updated."}, status=200)
    #     return Response(serializer.errors, status=400)


class ConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id_1, user_id_2, format=None):
        if request.user.id not in [int(user_id_1), int(user_id_2)]:
            return Response({"detail": "Unauthorized"}, status=403)

        messages = Message.objects.filter(
            Q(sender_id=user_id_1, recipient_id=user_id_2)
            | Q(sender_id=user_id_2, recipient_id=user_id_1)
        ).order_by("timestamp")

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
