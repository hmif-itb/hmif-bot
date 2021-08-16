import datetime

from linebot.models import (
    SourceGroup,
    SourceRoom,
    SourceUser
)

def text_contains(text, keywords, series=False, max_len=9999):
    if len(text) > max_len:
        return False

    if series:
        idx = 0
        for keyword in keywords:
            new_idx = text.find(keyword)
            if new_idx < idx:
                return False
            idx = new_idx
        return True
    
    for keyword in keywords:
        if (text.find(keyword) == -1):
            return False
    return True

def get_source_id(event):
    source_id = None
    if (isinstance(event.source, SourceGroup)):
        source_id = event.source.group_id
    if (isinstance(event.source, SourceRoom)):
        source_id = event.source.room_id
    if (isinstance(event.source, SourceUser)):
        source_id = event.source.user_id

    return source_id

def count_days_to_end_of_semester(today):
    cur_month = today.month
    if 1 <= cur_month <= 6: # Even semester ends in June
        end_month = 6
        last_date = 30
    elif 7 <= cur_month <= 12: # Odd semester ends in December
        end_month = 12
        last_date = 31
    last_day = datetime.date(today.year, end_month, last_date)
    time_delta = last_day - today
    return time_delta.days