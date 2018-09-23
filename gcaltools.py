import requests, re
import configparser
import urllib3
import datetime, time, json

# Read configs
config = configparser.ConfigParser()
config.read('config.ini')
config.sections()


def getThisWeekEvent():
    # Get monday
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    monday = today - datetime.timedelta(days=today.weekday())

    param = {
        'date' : int(time.mktime(monday.timetuple())),
        'duration': 6
    }
    data = {
        'method' : 'getEventsInDuration',
        'param' : json.dumps(param)
    }
    res = requests.get(config['API']['endpoint'], params=data, verify=False)
    if (res.status_code == 200):
        return res.content
    else:
        return None

def getTodayEvent():
    param = {
        'date' : int(time.time()),
        'duration': 0
    }
    data = {
        'method' : 'getEventsInDuration',
        'param' : json.dumps(param)
    }
    res = requests.post(config['API']['endpoint'], data=data, verify=False)
    if (res.status_code == 200):
        return res.content
    else:
        return None
    
if __name__ == '__main__':
    res = json.loads(getTodayEvent())
    
    if(res['status']):
        if(len(res['events']) > 0):
            for event in res['events']:
                print(event["name"])

