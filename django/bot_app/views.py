from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.utils.crypto import get_random_string
from .models import ChatHistory

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent
)
import os
import json

ACCESS_TOKEN = os.environ["MY_CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["MY_CHANNEL_SECRET"]

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# Create your views here.
class CallbackView(View):
    def post(self, request):
        signature = request.headers["X-Line-Signature"]

        body = request.body.decode(request.encoding)
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponse(status=400)
        print(body)

        return HttpResponse(status=200)
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@handler.add(MessageEvent)
def handle_message(evt):
    evt_chat = json.loads(str(evt))
    old_chat = ChatHistory.objects.filter(chat__contains={"source":{"userId":evt_chat['source']['userId']}}).last()
    ChatHistory.objects.create(chat=evt_chat)
    try:
        response_text = get_response_text(evt_chat, old_chat)

        line_bot_api.reply_message(
            evt.reply_token,
            TextMessage(text=response_text)
        )
    except:
        import traceback
        traceback.print_exc()

def get_response_text(evt_chat, old_chat):
    response_text = "none"
    if evt_chat["message"]["text"] == ">>utf8-encode":
        response_text = "応援ください！"
    if old_chat is not None:
        old_chat = old_chat.chat
        if old_chat["type"] != "message":
            return response_text
        if old_chat["message"]["text"] == ">>utf8-encode":
            response_text = evt_chat["message"]["text"].encode('utf-8').hex()

    return response_text

@handler.add(FollowEvent)
def handle_follow(evt):
    ChatHistory.objects.create(chat=str(evt))
    line_bot_api.reply_message(
        evt.reply_token,
        TextMessage(text="follow thx!")
    )

