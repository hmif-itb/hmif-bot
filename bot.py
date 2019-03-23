from datetime import datetime
from linebot import LineBotApi
from linebot.models import TextSendMessage
import json


class HMIFLineBotApi(LineBotApi):
    def __init__(self, channel_access_token):
        super(HMIFLineBotApi, self).__init__(channel_access_token)

    def reply_message_raw(self, reply_token, messages, timeout=None):
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        data = {
            'replyToken': reply_token,
            'messages': [message for message in messages]
        }

        super(HMIFLineBotApi, self)._post(
            '/v2/bot/message/reply', data=json.dumps(data), timeout=timeout
        )

    def send_events(self, line_event, title, events):
        if (len(events) > 0):
            contents = []
            for event in events:
                name = event.get('name')
                startdate = datetime.fromtimestamp(event.get('start')).strftime('%d %b')
                enddate = datetime.fromtimestamp(event.get('end')).strftime('%d %b')
                starttime = datetime.fromtimestamp(event.get('start')).strftime('%H:%M')
                endtime = datetime.fromtimestamp(event.get('end')).strftime('%H:%M')
                duration = '{} - {}'.format(starttime, endtime)
                if (event.get('allDay', False)):
                    duration = '{}'.format(startdate)
                elif (startdate != enddate):
                    duration = '{} {} - {} {}'.format(startdate, starttime, enddate, endtime)
                content = {
                    'type': 'box',
                    'layout': 'horizontal',
                    'contents': [
                        {
                            'type': 'text',
                            'text': startdate,
                            'align': 'start',
                            'weight': 'bold',
                            'flex': 2,
                            'size': 'xs'
                        },
                        {
                            'type': 'box',
                            'layout': 'vertical',
                            'contents': [
                                {
                                    'type': 'text',
                                    'text': name,
                                    'gravity': 'top',
                                    'size': 'xs',
                                    'color': '#007bff',
                                    'wrap': True
                                },
                                {
                                    'type': 'text',
                                    'text': duration,
                                    'gravity': 'bottom',
                                    'size': 'xxs',
                                    'color': '#999999'
                                }
                            ],
                            'flex': 8
                        }
                    ]
                }
                contents.append(content)

            response = {
                'type': 'flex',
                'altText': title,
                'contents': {
                    'type': 'bubble',
                    'header': {
                        'type': 'box',
                        'layout': 'vertical',
                        'contents': [
                            {
                                'type': 'text',
                                'text': title
                            }
                        ]
                    },
                    # 'hero': {
                    #     'type': 'image',
                    #     'aspectMode': 'fit',
                    #     'url': 'https://hmifbot.herokuapp.com/images/header.jpg'
                    # },
                    'body': {
                        'type': 'box',
                        'layout': 'vertical',
                        'contents': contents
                    }
                }
            }
            self.reply_message_raw(line_event.reply_token, response)
        else:
            response = TextSendMessage(text='Wah belum ada event nih!')
            self.reply_message(line_event.reply_token, response)
