import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import emoji
import re
import preprocessor
import seaborn as sns
import new_preprocessor
import helper
from urlextract import URLExtract

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = new_preprocessor.preprocess(data)
    st.dataframe(df)
    # fetch unique users
    user_list = df['user'].unique().tolist()
    # user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Analysis wrt",user_list)


    # Analysis
    if st.sidebar.button("Show Analysis "):
        num_messages,words,num_media_message,links = helper.fetch_stat(selected_user,df)
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media Shared")
            st.title(num_media_message)
        with col4:
            st.header("Total link Shared")
            st.title(links)

        if selected_user == "Overall":
            st.title("Most Busy user")
            x ,percentage_df= helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col2:
                st.dataframe(percentage_df)

        # # if st.sidebar.button("Common Word"):
        #     st.title("Most Common Word")
        #     common_word = helper.most_common_word(selected_user,df)
        #     fig,ax = plt.subplots()
        #     ax.barh(common_word[0],common_word[1])
        #     st.pyplot(fig)
            # st.dataframe(common_word)
    
    # Wordcloud

    
    
if st.sidebar.button("Show Word Cloud"):
    st.title("Word Cloud Generator")
    wordcloud = helper.create_wordcloud(selected_user, df)  
    
    # Display the word cloud image within Streamlit UI
    st.image(wordcloud.to_array(), use_column_width=True)
    
    # Display the matplotlib plot using st.pyplot()
    plt.figure(figsize=(10, 5))  # Set the size of the plot
    plt.imshow(wordcloud, interpolation='bilinear')  # Display the word cloud
    plt.axis('off')  # Turn off axis
    # st.pyplot(plt)  # Display the plot using Streamlit's st.pyplot()

# Most Common Word
if st.sidebar.button("Common Word"):
    st.title("Most Common Word")
    common_word = helper.most_common_word(selected_user,df)
    fig,ax = plt.subplots()
    ax.barh(common_word[0],common_word[1])
    st.pyplot(fig)
    # st.dataframe(common_word)


# Most Common Emoji 

if st.sidebar.button("Emoji Counter"):
    st.title("Emoji Analysis")
    emoji_df = helper.emoji_counter(selected_user,df)
    if len(emoji_df) == 0:
        st.write(f"No emoji is used by {selected_user}")
    else:
        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)




if st.sidebar.button("Monthly Timeline"):
    st.title("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user,df)
    fig,ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'],color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)



if st.sidebar.button("Daily Timeline"):
    st.title("Daily Timeline")
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='Green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


if st.sidebar.button("Activity map"):
    col1,col2 = st.columns(2)
    # st.title("Activity map")
    with col1:
        st.header("Most busy day")
        busy_day = helper.week_activity_map(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values,color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.header("Most busy month")
        busy_month = helper.month_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values,color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

if st.sidebar.button("Weekely Activity "):
    st.title("Weekly Activity Map")
    user_heatmap = helper.activity_heatmap(selected_user,df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)
