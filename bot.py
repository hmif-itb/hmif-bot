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

    def __create_left_box_content(self, event):
        startday = datetime.fromtimestamp(event.get('start')).strftime('%a')
        startdate = datetime.fromtimestamp(event.get('start')).strftime('%d %b')
        left_box_contents = []
        left_box_contents.append({
            'type': 'text',
            'text': startday,
            'gravity': 'top',
            'align': 'end',
            'weight': 'bold',
            'size': 'xs'
        })
        left_box_contents.append({
            'type': 'text',
            'text': startdate,
            'gravity': 'top',
            'align': 'end',
            'weight': 'bold',
            'size': 'xs'
        })
        return left_box_contents

    def __create_right_box_content(self, event):
        right_box_contents = []
        right_box_contents.append({
            'type': 'text',
            'text': event.get('name'),
            'gravity': 'top',
            'size': 'xs',
            'color': '#101010',
            'wrap': True
        })
        if (not event.get('allDay', False)):
            startdate = datetime.fromtimestamp(event.get('start')).strftime('%a %d %b')
            enddate = datetime.fromtimestamp(event.get('end')).strftime('%a %d %b')

            starttime = datetime.fromtimestamp(event.get('start')).strftime('%H:%M')
            endtime = datetime.fromtimestamp(event.get('end')).strftime('%H:%M')

            duration = '{} - {}'.format(starttime, endtime)
            if (startdate != enddate):
                duration = '{} {} - {} {}'.format(startdate, starttime, enddate, endtime)

            right_box_contents.append({
                'type': 'text',
                'text': duration,
                'gravity': 'bottom',
                'size': 'xxs',
                'color': '#999999'
            })
        if (len(event.get('desc', '')) > 0):
            right_box_contents.append({
                'type': 'text',
                'text': event.get('desc', ''),
                'gravity': 'bottom',
                'size': 'xxs',
                'color': '#999999'
            })
        if (len(event.get('location', '')) > 0):
            right_box_contents.append({
                'type': 'text',
                'text': event.get('location', ''),
                'gravity': 'bottom',
                'size': 'xxs',
                'color': '#999999'
            })
        return right_box_contents

    def send_events(self, line_event, title, events):
        if (len(events) > 0):
            contents = []
            for event in events:
                left_box_contents = self.__create_left_box_content(event)
                right_box_contents = self.__create_right_box_content(event)
                content = {
                    'type': 'box',
                    'layout': 'horizontal',
                    'spacing': 'xs',
                    'contents': [
                        {
                            'type': 'box',
                            'layout': 'vertical',
                            'contents': left_box_contents,
                            'flex': 2,
                        },
                        {
                            'type': 'box',
                            'layout': 'vertical',
                            'contents': right_box_contents,
                            'flex': 8,
                        }
                    ]
                }
                contents.append(content)

            response = {
                'type': 'flex',
                'altText': title,
                'contents': {
                    'type': 'bubble',
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
