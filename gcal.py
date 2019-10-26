import json
import requests
import sys
from utils import text_contains

endpoint = 'https://script.google.com/macros/s/AKfycbw9x9Y-9dQucsjVRoevf-QAB1kADg6Z7Sy8sS_424ueX8iRjNjU/exec'

def getStudentYearFromText(text_message):
    year = None

    if text_contains(text_message, ['untuk', 'bit'], series=True):
        year = 16
    elif text_contains(text_message, ['untuk', 'unix'], series=True):
        year = 17
    elif text_contains(text_message, ['untuk', 'decrypt'], series=True):
        year = 18

    return year

def eventIsAssignmentForYear(event, year):
    return event['name'].find(str(year) + ']') != -1

def eventFilterAssignmentByYear(events, year):
    filtered = []
    for event in events:
        if eventIsAssignmentForYear(event, year):
            filtered.append(event)
    return filtered

def getEvents(text_message, group_id, start_date=None, days=None):
    year = getStudentYearFromText(text_message)

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
            raise result.get('message')
        if year is not None:
            return eventFilterAssignmentByYear(result.get('result'), year)
        return result.get('result')
    else:
        raise Exception('request return with status code {}'.format(r.status_code))


if __name__ == '__main__':
    days = None if len(sys.argv) < 3 else sys.argv[2]
    start_date = None if len(sys.argv) < 4 else sys.argv[3]

    print(getEvents(start_date=start_date, days=days))
