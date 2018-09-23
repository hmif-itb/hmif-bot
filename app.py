import json
import traceback
from datetime import datetime

from flask import Flask, abort, request, send_from_directory
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (MessageEvent, StickerSendMessage, TextMessage,
                            TextSendMessage)

import gcaltools
from linebotapiraw import LineBotApiRaw

app = Flask(__name__)

line_bot_api = LineBotApiRaw('UE+D0Ot1CJIhR6/QxJnWW2GakEQW6XCXBltllhhI4PxRqHOA69BkaeWNCG4nSrw5q1RnDroACfFMD/yDYfj0+yWMy5GTfXZK6jIO5kJ4X/odeATHQRVxlfDA/LMddgJA4W2wRN9ea3hs5xVOfqbMpwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ed8de0ee82cfe03116bffbd74858569c')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body)

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

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory('images', path)



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
    if(isSimilar(splitted, ['ada', 'apa', 'aja'])):
        res = {"status":False}
        title = ""
        today = datetime.date.today()
        if(isSimilar(splitted, ['minggu', 'ini'])):
            res = gcaltools.getEvent(today - datetime.timedelta(days=today.weekday()+1),7)
            title = "Timeline HMIF - Minggu Ini"
        elif(isSimilar(splitted, ['minggu', 'depan'])):
            res = gcaltools.getEvent(today + datetime.timedelta(days=(7-today.weekday()-1)),7)
            title = "Timeline HMIF - Minggu Depan"
        elif(isSimilar(splitted, ['hari', 'ini'])):
            res = gcaltools.getEvent(today, 0)
            title = "Timeline HMIF - Hari Ini"
        elif(isSimilar(splitted, ['besok'])):
            res = gcaltools.getEvent(today + datetime.timedelta(days=1), 0)
            title = "Timeline HMIF - Besok"
        try:
            res = json.loads(res)
            if(res['status']):
                if(len(res['events']) > 0):
                    contents = []
                    for t in res['events']:
                        startdate = datetime.fromtimestamp(t["start"]).strftime('%d %b')
                        name = t["name"]
                        starttime = datetime.fromtimestamp(t["start"]).strftime('%H:%M')
                        endtime = datetime.fromtimestamp(t["end"]).strftime('%H:%M')
                        content = {
                            "type" : "box",
                            "layout" : "horizontal",
                            "contents" : [
                                {
                                    "type" : "text",
                                    "text" : startdate,
                                    "align" : "start",
                                    "weight" : "bold",
                                    "flex" : 2,
                                    "size" : "xs"
                                },
                                {
                                    "type" : "box",
                                    "layout" : "vertical",
                                    "contents" : [        
                                        {
                                            "type" : "text",
                                            "text" : name,
                                            "gravity" : "top",
                                            "size" : "xs",
                                            "color" : "#007bff"
                                        },
                                        {
                                            "type" : "text",
                                            "text" : starttime + " - " + endtime,
                                            "gravity" : "bottom",
                                            "size" : "xxs",
                                            "color" : "#999999"
                                        }
                                    ],
                                    "flex" : 8
                                }
                            ]
                        }
                        contents.append(content)
                    
                    response = {
                        "type" : "flex",
                        "altText" : title,
                        "contents" : {
                            "type" : "bubble",
                            "header" : {
                                "type" : "box",
                                "layout" : "vertical",
                                "contents" : [
                                    {
                                        "type" : "text",
                                        "text" : title
                                    }
                                ]
                            },
                            "hero" : {
                                "type" : "image",
                                "url" : "https://hmifbot.herokuapp.com/images/header.jpg"
                            },
                            "body" : {
                                "type" : "box",
                                "layout" : "vertical",
                                "contents" : contents
                            }
                        }
                    }
                else:
                    response = TextSendMessage(text='Wah minggu ini belum ada event nih!')
                line_bot_api.reply_message_raw(event.reply_token, response)
        except:
            traceback.print_exc()
        

if __name__ == "__main__":
    app.run()
