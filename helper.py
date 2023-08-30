import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import emoji
import re
from wordcloud import WordCloud
from collections import Counter

from urlextract import URLExtract
extract = URLExtract()





def fetch_stat(selected_user,df):
    # if (selected_user == "Overall"):
    #     num_messages = df.shape[0]
    #     word = []
    #     for message in df['message']:
    #         word.extend(message.split())
    #     return num_messages,len(word)
    # else :
    #     new_df =  df[df['user'] == selected_user]
    #     num_messages = new_df.shape[0]
    #    ` word = []
    #     for message in new_df['message']:
    #         word.extend(message.split())`
    #     return num_messages,len(word)

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    percentage_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
        
    return x,percentage_df

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['message'] != "group_notification"]
    temp = df[df['message'] != "<Media omitted>\n"]

    word = []
    for message in temp['message']:
        word.extend(message.split())
    
    resulting_string = " ".join(word)
    
    # Create the WordCloud object
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(resulting_string)
    
    return wordcloud

def most_common_word(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    temp = df[df['message'] != "group_notification"]
    temp = df[df['message'] != "<Media omitted>\n"]
    f = open("stopwords.txt",'r')
    stop_words = f.read()
    words =[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    common_word = pd.DataFrame(Counter(words).most_common(20))
    return common_word
    

def emoji_counter(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    word = []
    for message in df['message']:
        word.extend(message.split())
    emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2\U0001F170-\U0001F251]', flags=re.UNICODE)

    # Extract emojis from the list of strings
    emojis = []
    for text in word:
        emojis += emoji_pattern.findall(text)
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
    

def monthly_timeline(selected_user,df):
    # df['month_num'] = df['user_dates'].dt.month

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap