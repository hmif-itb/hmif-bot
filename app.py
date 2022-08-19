from bot_service import BotService
from flask import Flask, abort, request, send_from_directory, Response, current_app
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextMessage,
)
import logging
from config import config


app = Flask(__name__)
app.debug = True

BotService.init_bot(config.get('access_token'))
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


@app.route('/status', methods=['GET'])
def status():
    return Response('{"good": "momentos"}', status=418, mimetype='application/json')


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message: str = event.message.text
    message = message.lower().strip()

    return BotService(event, message).reply()


if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s] %(asctime)s $(filename)s:%(lineno)s : ',
                        level=logging.INFO)
    app.run()
