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
        startdate = datetime.fromtimestamp(event.get('start')).strftime('%a %d %b')
        enddate = datetime.fromtimestamp(event.get('end') - 1).strftime('%a %d %b')
        if (not event.get('allDay', False) or startdate != enddate):
            starttime = datetime.fromtimestamp(event.get('start')).strftime('%H:%M')
            endtime = datetime.fromtimestamp(event.get('end')).strftime('%H:%M')

            # event that last less than a day
            duration = '{} - {}'.format(starttime, endtime)
            if (startdate != enddate):
                if (event.get('allDay', False)):
                    # all day event that last more than a day
                    duration = '{} - {}'.format(startdate, enddate)
                else:
                    # event that last more than a day, but not all day
                    duration = '{} {} - {} {}'.format(startdate, starttime, enddate, endtime)
            else:
                if (event.get('end') - event.get('start') <= 10 * 60):
                    # event that exist only as a mark, not event
                    duration = '{}'.format(starttime)

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
                'color': '#999999',
                'wrap': True
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

    def __wrap_event_row(self, left_box_contents, right_box_contents):
        return {
            'type': 'box',
            'layout': 'horizontal',
            'spacing': 'md',
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

    def __wrap_event_message(self, title, contents):
        return {
            'type': 'flex',
            'altText': title,
            'contents': {
                'type': 'bubble',
                'body': {
                    'type': 'box',
                    'layout': 'vertical',
                    'spacing': 'md',
                    'contents': contents,
                }
            }
        }

    def __split_list(self, data, n):
        chunks = [data[x:x + n] for x in range(0, len(data), n)]
        return chunks

    def send_events(self, line_event, title, events):
        if (len(events) > 0):
            rows = []
            for event in events:
                left_box_contents = self.__create_left_box_content(event)
                right_box_contents = self.__create_right_box_content(event)
                content = self.__wrap_event_row(left_box_contents, right_box_contents)
                rows.append(content)

            messages = []
            n_break = 12
            chunks = self.__split_list(rows, n_break)

            for chunk in chunks:
                message = self.__wrap_event_message(title, chunk)
                messages.append(message)

            print(f'Sending {len(events)} events in {len(messages)} messages..')

            self.reply_message_raw(line_event.reply_token, messages[:5])
        else:
            response = TextSendMessage(text='Wah belum ada event nih!')
            self.reply_message(line_event.reply_token, response)
