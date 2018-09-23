import requests, re
import configparser
import urllib3
import datetime, time, json

# Read configs
config = configparser.ConfigParser()
config.read('config.ini')
config.sections()
def getEvent(date, duration):
    param = {
        'date' : int(int(time.mktime(date.timetuple()))),
        'duration': int(duration)
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
    
if __name__ == '__main__':
    today = datetime.date.today()
    res = json.loads(getEvent(today - datetime.timedelta(days=today.weekday()+1),7))
    print(res)
    if(res['status']):
        if(len(res['events']) > 0):
            for event in res['events']:
                print(event["name"])

