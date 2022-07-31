import datetime
import gcal
import re
import random

from flask import Flask, abort, request, send_from_directory, Response
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
from utils import (
    text_contains,
    get_source_id,
    count_days_to_end_of_semester,
)
from replies import (replies_massa, reply_help,
                     reply_help_deadline, reply_help_seminar, reply_help_ujian)


app = Flask(__name__)
app.debug = True

hmif_bot = HMIFLineBotApi(config.get('access_token'))
handler = WebhookHandler(config.get('secret'))


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


@app.route('/status')
def status():
    return Response("{}", status=418, mimetype='application/json')


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    message = message.lower()

    # Handle help message
    if (message == 'help hmif bot'):
        response = TextSendMessage(text=reply_help)
        try:
            hmif_bot.reply_message(event.reply_token, response)
        except Exception as e:
            print(e)
        return

        # Handle help message
    if (message == 'help hmif bot deadline'):
        response = TextSendMessage(text=reply_help_deadline)
        try:
            hmif_bot.reply_message(event.reply_token, response)
        except Exception as e:
            print(e)
        return

    if ((message == 'help hmif bot seminar') or (message == 'help hmif bot sidang')):
        response = TextSendMessage(text=reply_help_seminar)
        try:
            hmif_bot.reply_message(event.reply_token, response)
        except Exception as e:
            print(e)
        return

    if ((message == 'help hmif bot ujian')):
        response = TextSendMessage(text=reply_help_ujian)
        try:
            hmif_bot.reply_message(event.reply_token, response)
        except Exception as e:
            print(e)
        return

    # Handle calendar messages
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
            start_date = today + \
                datetime.timedelta(days=(7 - today.weekday() - 1))
            days = 7
        elif (text_contains(message, ['hari', 'ini'], series=True)):
            title = "Timeline HMIF - Hari Ini"
            start_date = today
            days = 0
        elif (text_contains(message, ['besok'], series=True)):
            title = "Timeline HMIF - Besok"
            start_date = today + datetime.timedelta(days=1)
            days = 0
        elif (text_contains(message, ['sejauh', 'ini'], series=True)):
            title = "Timeline HMIF - Deadline Sejauh Ini"
            start_date = today
            days = count_days_to_end_of_semester(today)

        source_id = get_source_id(event)
        print(source_id)
        events = gcal.getEvents(
            message, source_id, start_date=start_date, days=days)

        try:
            hmif_bot.send_events(event, title, events)
        except Exception as e:
            print(e)
    elif (message == '/uid'):
        source_id = get_source_id(event)
        response = TextSendMessage(text=source_id)
        try:
            hmif_bot.reply_message(event.reply_token, response)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app.run()
