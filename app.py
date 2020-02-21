import datetime
import gcal
import re
import random

from flask import Flask, abort, request, send_from_directory
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    ImageSendMessage,
    MessageEvent,
    SourceGroup,
    SourceRoom,
    SourceUser,
    TextMessage,
    TextSendMessage,
)

from bot import HMIFLineBotApi
from config import config
from utils import text_contains


app = Flask(__name__)
app.debug = True

hmif_bot = HMIFLineBotApi(config.get('access_token'))
handler = WebhookHandler(config.get('secret'))

'''
# Commented, because this is specific request from HMIF President 19/20
replies_massa = [
    TextSendMessage(text='M****? KARTU KUNING MAS MBA!'),
    TextSendMessage(text='Ga ada m*ss* di HMIF, adanya anggota'),
    TextSendMessage(text='M****? Tolong ini ditendang dong'),
    TextSendMessage(text='Eh siapa bilang m****? Ntar dicubit Deborah lho'),
    ImageSendMessage(original_content_url='https://hmif-bot.herokuapp.com/images/Meme-1.png',
                     preview_image_url='https://hmif-bot.herokuapp.com/images/Meme-1.png'),
    ImageSendMessage(original_content_url='https://hmif-bot.herokuapp.com/images/Meme-2.png',
                     preview_image_url='https://hmif-bot.herokuapp.com/images/Meme-2.png'),
]
'''

replies_abay = [
    ImageSendMessage(original_content_url='https://hmif-bot.herokuapp.com/images/abay_1.jpg',
                     preview_image_url='https://hmif-bot.herokuapp.com/images/abay_1.jpg'),
    ImageSendMessage(original_content_url='https://hmif-bot.herokuapp.com/images/abay_2.jpg',
                     preview_image_url='https://hmif-bot.herokuapp.com/images/abay_2.jpg'),
    ImageSendMessage(original_content_url='https://hmif-bot.herokuapp.com/images/abay_3.jpg',
                     preview_image_url='https://hmif-bot.herokuapp.com/images/abay_3.jpg'),
    ImageSendMessage(original_content_url='https://hmif-bot.herokuapp.com/images/abay_4.jpg',
                     preview_image_url='https://hmif-bot.herokuapp.com/images/abay_4.jpg'),
    ImageSendMessage(original_content_url='https://hmif-bot.herokuapp.com/images/abay_5.jpg',
                     preview_image_url='https://hmif-bot.herokuapp.com/images/abay_5.jpg'),
    ImageSendMessage(original_content_url='https://hmif-bot.herokuapp.com/images/abay_6.jpg',
                     preview_image_url='https://hmif-bot.herokuapp.com/images/abay_6.jpg'),
    ImageSendMessage(original_content_url='https://hmif-bot.herokuapp.com/images/abay_7.jpg',
                     preview_image_url='https://hmif-bot.herokuapp.com/images/abay_7.jpg'),
    ImageSendMessage(original_content_url='https://hmif-bot.herokuapp.com/images/abay_8.jpg',
                     preview_image_url='https://hmif-bot.herokuapp.com/images/abay_8.jpg'),
    ImageSendMessage(original_content_url='https://hmif-bot.herokuapp.com/images/abay_9.jpg',
                     preview_image_url='https://hmif-bot.herokuapp.com/images/abay_9.jpg'),
]


@app.route("/line-webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

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
def send_images(path):
    return send_from_directory('images', path)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    message = message.lower()

    # Handle messages
    if (text_contains(message, ['ada', 'apa', 'aja'], series=True, max_len=75)):
        today = datetime.date.today()
        title = ""
        start_date = None
        days = None

        if (text_contains(message, ['bulan', 'ini'], series=True)):
            title = "Timeline HMIF - Bulan Ini"
            start_date = today
            days = 30
        elif (text_contains(message, ['minggu', 'ini'], series=True)):
            title = "Timeline HMIF - Minggu Ini"
            start_date = today
            days = 7
        elif (text_contains(message, ['minggu', 'depan'], series=True)):
            title = "Timeline HMIF - Minggu Depan"
            start_date = today + datetime.timedelta(days=(7 - today.weekday() - 1))
            days = 7
        elif (text_contains(message, ['hari', 'ini'], series=True)):
            title = "Timeline HMIF - Hari Ini"
            start_date = today
            days = 0
        elif (text_contains(message, ['besok'], series=True)):
            title = "Timeline HMIF - Besok"
            start_date = today + datetime.timedelta(days=1)
            days = 0

        source_id = None
        if (isinstance(event.source, SourceGroup)):
            source_id = event.source.group_id
        if (isinstance(event.source, SourceRoom)):
            source_id = event.source.room_id
        if (isinstance(event.source, SourceUser)):
            source_id = event.source.user_id
        print(source_id)
        events = gcal.getEvents(message, source_id, start_date=start_date, days=days)

        try:
            hmif_bot.send_events(event, title, events)
        except Exception as e:
            print(e)
    elif (text_contains(message, ['massa'], max_len=10)):
        response = TextSendMessage(text='Siapa massa... eh abay dah turun deng hehe ')
        try:
            hmif_bot.reply_message(event.reply_token, response)
        except Exception as e:
            print(e)
    elif (re.compile(r"\ba?bay+\b", re.I | re.M).search(message) and len(message) <= 30):
        response = random.choice(replies_abay)
        try:
            hmif_bot.reply_message(event.reply_token, response)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app.run()
