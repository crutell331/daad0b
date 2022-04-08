async_mode = None

import os
import pdb
import json
from django.db.models import Max, Q

import socketio
from online_users import online_users
from messenger_backend.models import Conversation, Message

basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(async_mode=async_mode, logger=False)
thread = None


@sio.event
def connect(sid, environ):
    sio.emit("my_response", {"data": "Connected", "count": 0}, room=sid)



@sio.on("go-online")
def go_online(sid, user_id):
    if user_id not in online_users:
        online_users.append(user_id)
    sio.emit("add-online-user", user_id, skip_sid=sid)


@sio.on("new-message")
def new_message(sid, message):
    sio.emit(
        "new-message",
        {"message": message["message"], "sender": message["sender"]},
        skip_sid=sid,
    )


@sio.on("logout")
def logout(sid, user_id):
    if user_id in online_users:
        online_users.remove(user_id)
    sio.emit("remove-offline-user", user_id, skip_sid=sid)

@sio.on("read-message")
def read_message(sid, data):
    # pdb.set_trace()
    convo = Conversation.objects.get(pk=data["conversationId"])
    other_user_id = data["otherUserId"]
    # messages = [
    #     message.to_dict(["id", "text", "senderId", "read"])
    #         for message in convo.messages.all()
    #     ]
    # for message in convo.messages.all():
    #     messages.append(message.to_dict(["id", "text", "senderId", "createdAt", "read"]))

    # pdb.set_trace()
    lastReadMessage = None
    if convo.messages.all().filter(Q(read=True) & Q(senderId=other_user_id)).last(): 
        lastReadMessage = convo.messages.all().filter(Q(read=True) & Q(senderId=other_user_id)).last().id

    # pdb.set_trace()
    sio.emit("read-message",
        {"conversationId": data['conversationId'], "otherUserId": data['otherUserId'], "lastReadMessage": lastReadMessage}
    )