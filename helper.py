from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
def filter_messages(selected_df,df):
    if selected_df != 'Overall':
        df = df[df['users']==selected_df]
    return df

def fetch_stats(selected_df,df):
    # Total messages
    df = filter_messages(selected_df,df)
    no_of_msg = df.shape[0]

    # total words
    words = []
    for msg in df['messages']:
        words.extend(msg.split())

    # links shared

    links = []
    extractor = URLExtract()
    for i in df['messages']:
        links.extend(extractor.find_urls(i))



    return no_of_msg,len(words),len(links)
def removing_stopwords(df):

    with open('stop_hinglish.txt','r',encoding='utf-8') as f:
        hinglish_stopwords = f.read().splitlines()
    english_stopwords = stopwords.words('english')
    all_stopwords = set(hinglish_stopwords + english_stopwords)

    words = []
    for msg in df['messages']:
        for word in msg.lower().split():
            if word not in all_stopwords:
                words.append(word)

    return words
def create_word_cloud(selected_df,df):
    df = filter_messages(selected_df, df)
    word  = removing_stopwords(df)


    from wordcloud import WordCloud
    wc = WordCloud(height=500, width=500, min_font_size=10, background_color='white')
    dc = wc.generate(' '.join(word))
    return dc


def most_common_words(selected_df,df):
    df = filter_messages(selected_df, df)
    words = removing_stopwords(df)
    common_words = pd.DataFrame(Counter(words).most_common(20),columns=['word', 'count'])
    return common_words

def helper_emoji(selected_df,df):

    df = filter_messages(selected_df, df)


    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

def monthly_timeline(selected_df,df):

    df = filter_messages(selected_df, df)
    timeline = df.groupby(['year', 'month', 'month_name']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append((timeline['month_name'][i] + "-" + str(timeline['year'][i])))
    timeline['time'] = time
    return timeline
def daily_timeline(selected_df,df):
    df = filter_messages(selected_df, df)
    daily = df.groupby('only date')['messages'].count().reset_index()
    return daily
def activity_map(selected_df,df):
    df = filter_messages(selected_df, df)
    return df['day_name'].value_counts()

def month_activity_map(selected_df,df):
    df = filter_messages(selected_df, df)
    return  df['month_name'].value_counts()



def activity_heatmap(selected_df,df):
    df = filter_messages(selected_df, df)

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)
    return user_heatmap



