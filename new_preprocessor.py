import pandas as pd
import re

# f = open('chat.txt','r',encoding='utf-8')
# data = f.read()
def preprocess(data):
    pattern = '\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}:\d{1,2}]'
    message = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({"user_message":message,"user_dates":dates})
    df['user_dates'] = pd.to_datetime(df["user_dates"],format="[%d/%m/%y, %H:%M:%S]")
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name 
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['user_dates'].dt.year
    df['month'] = df['user_dates'].dt.month_name()
    df['day'] = df['user_dates'].dt.day_name
    df['hour'] = df['user_dates'].dt.hour
    df['minute'] = df['user_dates'].dt.minute
    # df.drop(columns=["user_dates"], inplace=True)
    df['month_num'] = df['user_dates'].dt.month
    df['only_date'] = df['user_dates'].dt.date
    df['day_name'] = df['user_dates'].dt.day_name()
    


    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df