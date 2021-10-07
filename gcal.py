import json
import requests
import sys
from utils import text_contains, text_contains_or

endpoint = 'https://script.google.com/macros/s/AKfycbx0YswIakU6mXgXvPy-WuGLHnOaPqnsFzdk1jBcX4pPw0XdZu6g8F6CXXjfERSJIN93kA/exec'


def getStudentYearFromText(text_message):
    year = None

    if text_contains(text_message, ['untuk', 'bit'], series=True) or text_contains(text_message, ['untuk', '16'], series=True):
        year = 16
    elif text_contains(text_message, ['untuk', 'unix'], series=True) or text_contains(text_message, ['untuk', '17'], series=True):
        year = 17
    elif text_contains(text_message, ['untuk', 'decrypt'], series=True) or text_contains(text_message, ['untuk', '18'], series=True):
        year = 18
    elif text_contains(text_message, ['untuk', 'async'], series=True) or text_contains(text_message, ['untuk', '19'], series=True):
        year = 19
    elif text_contains(text_message, ['untuk', 'init'], series=True) or text_contains(text_message, ['untuk', '20'], series=True):
        year = 20

    return year


def getStudentMajorFromText(text_message):
    major = None

    if text_contains(text_message, ['if']):
        major = 'IF'
    elif text_contains(text_message, ['sti']):
        major = 'STI'

    return major


def eventIsAssignmentForYear(event, year):
    return event['name'].find(str(year) + ']') != -1


def eventFilterAssignmentByYear(events, year):
    filtered = []
    for event in events:
        if eventIsAssignmentForYear(event, year):
            filtered.append(event)
    return filtered


def eventIsAssignmentForMajor(event, major):
    return event['name'].find('[' + major) != -1


def eventFilterAssignmentByMajor(events, major):
    filtered = []
    for event in events:
        if eventIsAssignmentForMajor(event, major):
            filtered.append(event)
    return filtered


def eventFilterByContext(events, context):
    filtered = []
    keywordUjian = ["UAS", "UTS"]
    for event in events:
        eventName = event.get('name')
        print(eventName)
        isEventUjian = text_contains_or(eventName, keywordUjian)
        if context == "ujian" and isEventUjian:
            filtered.append(event)
        elif context == "deadline" and (not isEventUjian):
            filtered.append(event)
    return filtered


def getContextFromText(text_message):
    if text_message.find("ujian") != -1:
        return "ujian"
    return "deadline"


def getEvents(text_message, group_id, start_date=None, days=None):
    year = getStudentYearFromText(text_message)
    major = getStudentMajorFromText(text_message)

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

    r = requests.get(endpoint, params=data, verify=False)
    if (r.status_code == 200):
        result = json.loads(str(r.content, 'utf-8'))
        if (result.get('code') != 'SUCCESS'):
            raise Exception(result.get('code'))
        events = result.get('result')
        if year is not None:
            events = eventFilterAssignmentByYear(events, year)
        if major is not None:
            events = eventFilterAssignmentByMajor(events, major)
        context = getContextFromText(text_message)
        events = eventFilterByContext(events, context)
        return events
    else:
        raise Exception(
            'request return with status code {}'.format(r.status_code))


if __name__ == '__main__':
    days = None if len(sys.argv) < 2 else int(sys.argv[1])
    start_date = None if len(sys.argv) < 3 else sys.argv[2]

    text_message = "ada ujian apa aja minggu ini untuk sti 18"
    group_id = "group_id"

    print(getEvents(text_message, group_id, start_date=start_date, days=days))
