import pdb
from django.contrib.auth.middleware import get_user
from django.db.models import Max, Q
from django.db.models.query import Prefetch
from django.http import HttpResponse, JsonResponse
from messenger_backend.models import Conversation, Message
from online_users import online_users
from rest_framework.views import APIView
from rest_framework.request import Request


class Conversations(APIView):
    """get all conversations for a user, include latest message text for preview, and all messages
    include other user model so we have info on username/profile pic (don't include current user info)
    TODO: for scalability, implement lazy loading"""

    def get(self, request: Request):
        try:
            user = get_user(request)

            if user.is_anonymous:
                return HttpResponse(status=401)
            user_id = user.id

            conversations = (
                Conversation.objects.filter(Q(user1=user_id) | Q(user2=user_id))
                .prefetch_related(
                    Prefetch(
                        "messages", queryset=Message.objects.order_by("-createdAt").reverse() # reverse the order of the list so most recent message is last and the oldest message is first
                    )
                )
                .all()
            )

            conversations_response = []
            for convo in conversations:
                lastReadMessage = None
                
                # retrieve last message sent by user that was read and add to dictionary otherwise None
                if convo.messages.all().filter(Q(read=True) & Q(senderId=user.id)).last(): lastReadMessage = convo.messages.all().filter(Q(read=True) & Q(senderId=user.id)).last().id
                convo_dict = {
                    "id": convo.id,
                    "messages": [
                        message.to_dict(["id", "text", "senderId", "createdAt", "read"])
                        for message in convo.messages.all()
                    ],
                    "lastReadMessage": lastReadMessage
                }

                # set properties for notification count and latest message preview
                convo_dict["latestMessageText"] = convo_dict["messages"][-1]["text"]

                # set a property "otherUser" so that frontend will have easier access
                user_fields = ["id", "username", "photoUrl"]
                if convo.user1 and convo.user1.id != user_id:
                    convo_dict["otherUser"] = convo.user1.to_dict(user_fields)
                elif convo.user2 and convo.user2.id != user_id:
                    convo_dict["otherUser"] = convo.user2.to_dict(user_fields)

                # set property for online status of the other user
                if convo_dict["otherUser"]["id"] in online_users:
                    convo_dict["otherUser"]["online"] = True
                else:
                    convo_dict["otherUser"]["online"] = False

                conversations_response.append(convo_dict)

            conversations_response.sort(
                key=lambda convo: convo["messages"][0]["createdAt"],
                reverse=True,
            )
            return JsonResponse(
                conversations_response,
                safe=False,
            )
        except Exception as e:
            return HttpResponse(status=500)


    def patch(self, request):
        user = get_user(request)

        if user.is_anonymous:
            return HttpResponse(status=401)

        conversation_id = request.data['conversationId']
        other_user_id = request.data['otherUserId']
        
        conversation = Conversation.objects.get(pk=conversation_id)
        user_messages = conversation.messages.filter(Q(senderId = other_user_id))

        objs = []
        for message in user_messages:
            obj = message
            obj.read = True
            objs.append(obj)

        Message.objects.bulk_update(objs, ['read'])

        return HttpResponse(status=204)
      
