from utils import text_contains, text_contains_or
import json
import requests
import sys
import urllib3

requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GcalService:
    __gcal_endpoint = 'https://script.google.com/macros/s/AKfycbwXSY3FWlFOIUXiC7wpR--3aVfLbRUKoQBVcL9GtrvA2f2t1vFEOPpUASOLgUn5fTNl/exec'  # noqa

    # public methods (ORDER ALPHABETICALLY)
    def get_events(text_message, group_id, start_date=None, days=None):
        if text_message is None or group_id is None:
            raise ValueError('text_message or group_id cannot be None')
        year = GcalService.__get_student_year_from_text(text_message)
        major = GcalService.__get_student_major_from_text(text_message)

        param = dict()
        param['textMessage'] = text_message
        param['groupId'] = group_id
        if (start_date is not None):
            param['startDate'] = start_date.strftime('%Y-%m-%d')
        if (days is not None):
            param['days'] = days

        data = dict()
        data['action'] = 'getEventsByDuration'
        data['param'] = json.dumps(param)

        r = requests.get(GcalService.__gcal_endpoint, params=data, verify=False)
        if (r.status_code != 200):
            raise Exception('request return with status code {}'.format(r.status_code))

        try:
            content = str(r.content, 'utf-8')
            result = json.loads(content)
        except json.decoder.JSONDecodeError:
            raise Exception("Can't decode JSON: " + content)

        if (result.get('code') != 'SUCCESS'):
            raise Exception(result.get('code') + ' is not SUCCESS')

        events = result.get('result')
        if year is not None:
            events = GcalService.__event_filter_assignment_by_year(events, year)
        if major is not None:
            events = GcalService.__event_filter_assignment_by_major(events, major)
        context = GcalService.__get_context_from_text(text_message)
        events = GcalService.__event_filter_by_context(events, context)
        return events

    # private helper methods (ORDER ALPHABETICALLY)
    def __event_filter_assignment_by_major(events, major):
        filtered = []
        for event in events:
            if GcalService.__event_is_assignment_for_major(event, major):
                filtered.append(event)
        return filtered

    def __event_filter_assignment_by_year(events, year):
        filtered = []
        for event in events:
            if GcalService.__event_is_assignment_for_year(event, year):
                filtered.append(event)
        return filtered

    def __event_filter_by_context(events, context):
        filtered = []
        keywordUjian = ["UAS", "UTS"]
        for event in events:
            eventName = event.get('name')
            isEventUjian = text_contains_or(eventName, keywordUjian)
            if context == "ujian" and isEventUjian:
                filtered.append(event)
            elif context == "deadline" and (not isEventUjian):
                filtered.append(event)
        return filtered

    def __event_is_assignment_for_major(event, major):
        return event['name'].find('[' + major) != -1

    def __event_is_assignment_for_year(event, year):
        return event['name'].find(str(year) + ']') != -1

    def __get_context_from_text(text_message):
        '''
        context is "ujian" or "deadline"
        '''
        if text_message.find("ujian") != -1:
            return "ujian"
        return "deadline"

    def __get_student_major_from_text(text_message):
        major = None

        if text_contains(text_message, ['if']):
            major = 'IF'
        elif text_contains(text_message, ['sti']):
            major = 'STI'

        return major

    def __get_student_year_from_text(text_message):
        year = None

        if (text_contains(text_message, ['untuk', 'bit'], series=True)
                or text_contains(text_message, ['untuk', '16'], series=True)):
            year = 16
        elif (text_contains(text_message, ['untuk', 'unix'], series=True)
                or text_contains(text_message, ['untuk', '17'], series=True)):
            year = 17
        elif (text_contains(text_message, ['untuk', 'decrypt'], series=True)
                or text_contains(text_message, ['untuk', '18'], series=True)):
            year = 18
        elif (text_contains(text_message, ['untuk', 'async'], series=True)
                or text_contains(text_message, ['untuk', '19'], series=True)):
            year = 19
        elif (text_contains(text_message, ['untuk', 'init'], series=True)
                or text_contains(text_message, ['untuk', '20'], series=True)):
            year = 20
        elif (text_contains(text_message, ['untuk', 'sudo'], series=True)
                or text_contains(text_message, ['untuk', '21'], series=True)):
            year = 21

        return year


if __name__ == '__main__':
    days = None if len(sys.argv) < 2 else int(sys.argv[1])
    start_date = None if len(sys.argv) < 3 else sys.argv[2]

    text_message = "ada ujian apa aja minggu ini untuk sti 18"
    group_id = "group_id"

    print(GcalService.getEvents(text_message, group_id, start_date=start_date, days=days))
