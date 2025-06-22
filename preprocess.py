import re
import pandas as pd
def process(data):
    from datetime import datetime

    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:[\s\u202f]?[APMapm]{2})?\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    new_dates = []
    for d in dates:
        new_dates.append(d.replace('\u202f', ' ').replace(' -', '').strip())


    df = pd.DataFrame({'user_messages': messages, 'dates': new_dates})

    def parse_datetime(s):
        formats = [
            "%d/%m/%y, %I:%M %p",  # 12-hour, day/month/year
            "%m/%d/%y, %I:%M %p",  # 12-hour, month/day/year
            "%d/%m/%y, %H:%M",  # 24-hour, day/month/year
            "%m/%d/%y, %H:%M",  # 24-hour, month/day/year
            "%d/%m/%Y, %I:%M %p",  # 4-digit year 12h
            "%d/%m/%Y, %H:%M",  # 4-digit year 24h
        ]

        for fmt in formats:
            try:
                return datetime.strptime(s, fmt)
            except:
                continue
        return None

    df['datetime'] = df['dates'].apply(parse_datetime)
    user = []
    msg = []
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            user.append(entry[1])
            msg.append(entry[2])
        else:
            user.append('group_notification')
            msg.append(entry[0])

    df['users'] = user
    df['messages'] = msg
    df.drop(columns=['user_messages'], inplace=True, axis=1)
    df.drop(columns=['dates'], inplace=True, axis=1)
    df['year'] = df['datetime'].dt.year
    df['month_name'] = df['datetime'].dt.month_name()
    df['month'] = df['datetime'].dt.month
    df['hours'] = df['datetime'].dt.hour
    df['minutes'] = df['datetime'].dt.minute
    df['only date'] = df['datetime'].dt.date
    df['day_name'] = df['datetime'].dt.day_name()
    period = []
    for hour in df[['day_name', 'hours']]['hours']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    df = df[df['users'] != 'group_notification']
    df = df[~df['messages'].str.contains('<Media omitted>')]
    return df