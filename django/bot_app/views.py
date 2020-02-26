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
from random import randint

ACCESS_TOKEN = os.environ["MY_CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["MY_CHANNEL_SECRET"]

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

post_user_state = {}
# Create your views here.
class CallbackView(View):
    def post(self, request):
        signature = request.headers["X-Line-Signature"]

        body = request.body.decode(request.encoding)
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponse(status=400)

        ChatHistory.objects.create(chat=json.loads(body))

        return HttpResponse(status=200)
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@handler.add(MessageEvent)
def handle_message(evt):
    if evt.source.user_id not in post_user_state:
        post_user_state[evt.source.user_id] = {"state": None, "bit_state": 16}
    user = post_user_state[evt.source.user_id]
    try:
        response_text = get_response_text(evt, user)

        line_bot_api.reply_message(
            evt.reply_token,
            TextMessage(text=response_text)
        )
    except:
        import traceback
        traceback.print_exc()

def get_response_text(evt, user):
    response_text = "none"
    evt_text = evt.message.text

    if user['state'] == ">> utf8-encode":
        response_text = evt_text.encode('utf-8').hex()
        user["state"] = None
    elif user['state'] == ">> utf8-decode":
        try:
            response_text = bytes.fromhex(evt_text).decode('utf-8')
        except:
            response_text = "失敗しちゃった…"
        user["state"] = None
    elif user['state'] in [">> xy", ">> x/y", ">> x^y mod z"]:
        try:
            tmp = int(evt_text, user["bit_state"])
        except ValueError:
            response_text = f"{user['bit_state']}進数じゃないの入れたでしょ！？"
        except:
            response_text = "内部エラー"
        if "x" not in user:
            user["x"] = tmp
            response_text = "yの値は?"
        elif "y" not in user:
            user["y"] = tmp
            response_text = "zの値は?"
            if user['state'] == ">> xy":
                response_text = hex(user["x"]*user["y"])[2:]
                user["state"] = None
                del user["x"], user["y"]
            elif user['state'] == ">> x/y":
                response_text = hex(user["x"]//user["y"])[2:]
                user["state"] = None
                del user["x"], user["y"]
        elif user["state"] == ">> x^y mod z":
            response_text = hex(pow(user["x"], user["y"], tmp))[2:]
            user["state"] == None
            del user["x"], user["y"]

    if evt_text == ">> utf8-encode":
        response_text = "応援ください！"
    elif evt_text == ">> utf8-decode":
        response_text = "ガンバリマス！"
    elif evt_text == ">> x^y mod z":
        response_text = "xの値は?"
    elif evt_text == ">> xy":
        response_text = "xの値は?"
    elif evt_text == ">> x/y":
        response_text = "xの値は?"
    else:
        return response_text
    
    user['state'] = evt_text
    return response_text

@handler.add(FollowEvent)
def handle_follow(evt):
    ChatHistory.objects.create(chat=str(evt))
    line_bot_api.reply_message(
        evt.reply_token,
        TextMessage(text="follow thx!")
    )

