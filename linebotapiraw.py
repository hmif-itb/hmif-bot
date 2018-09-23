from linebot import LineBotApi
import json

class LineBotApiRaw(LineBotApi):
    def __init__(self, channel_access_token):
        super(LineBotApiRaw, self).__init__(channel_access_token)

    def reply_message_raw(self, reply_token, messages, timeout=None):
        if not isinstance(messages, (list, tuple)):
            messages = [messages]
        
        data = {
            'replyToken': reply_token,
            'messages': [message for message in messages]
        }
        
        super(LineBotApiRaw, self)._post(
            '/v2/bot/message/reply', data=json.dumps(data), timeout=timeout
        )