from flask import Flask, request, abort
import gcaltools
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('UE+D0Ot1CJIhR6/QxJnWW2GakEQW6XCXBltllhhI4PxRqHOA69BkaeWNCG4nSrw5q1RnDroACfFMD/yDYfj0+yWMy5GTfXZK6jIO5kJ4X/odeATHQRVxlfDA/LMddgJA4W2wRN9ea3hs5xVOfqbMpwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ed8de0ee82cfe03116bffbd74858569c')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'


def isSimilar(message, template):
	similarity = len(template)
	
	for t in template:
		if(t in message):
			similarity -= 1
	return similarity == 0
	
	
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    message = message.lower()
    splitted = message.split(' ')

    # Handle messages
    if(isSimilar(splitted, ['ini', 'ada', 'apa', 'aja'])):
        if(isSimilar(splitted, ['minggu'])):
            event = gcaltools.getThisWeekEvent()
            
        elif(isSimilar(splitted, ['hari'])):
            event = gcaltools.getTodayEvent()

if __name__ == "__main__":
    app.run()