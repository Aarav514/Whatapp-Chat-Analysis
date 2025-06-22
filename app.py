import streamlit as st
import preprocess
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📊 WhatsApp Chat Analyzer")
st.markdown("Upload your WhatsApp chat `.txt` file to get detailed insights and visualizations.")

st.sidebar.title('Whatsapp Chat Analysis')
uploaded_file = st.sidebar.file_uploader('Choose a Whatsapp file for Analysis')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocess.process(data)

    # fetch unique users
    user_list = df['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_df = st.sidebar.selectbox('Show Analysis wrt',user_list)
    if st.sidebar.button('Show Analysis'):
        st.title('Top Statistics')
        num_messages,num_words,num_links = helper.fetch_stats(selected_df,df)
        col1,col2,col3 = st.columns(3)
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(num_words)
        with col3:
            st.header('No of Links Shared')
            st.title(num_links)

        # Monthly Timeline
        timeline = helper.monthly_timeline(selected_df, df)
        st.header('Monthly Timeline')
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title('Daily Timeline')
        daily = helper.daily_timeline(selected_df, df)
        fig, ax = plt.subplots()
        ax.plot(daily['only date'],daily['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Activity Map
        st.title('Activity Map')
        col1,col2 = st.columns(2)
        with col1:
            st.header('Most Busy Days')
            busy_days = helper.activity_map(selected_df, df)
            fig,ax = plt.subplots()
            ax.bar(busy_days.index,busy_days.values)
            st.pyplot(fig)
        with col2:
            st.header('Busy Months')

            busy_month = helper.month_activity_map(selected_df, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)







        # finding the busiest users in the group(Group level)
        if selected_df == 'Overall':
            x = df['users'].value_counts().head()
            st.title('Top Busy Users')
            col1,col2 = st.columns(2)
            with col1:
                fig,ax = plt.subplots()
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            y = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
                columns={'count': 'percentage'})
            with col2:
                st.dataframe(y)

        word_coud = helper.create_word_cloud(selected_df, df)
        st.header('WordCloud')
        fig, ax = plt.subplots()
        plt.imshow(word_coud)
        st.pyplot(fig)


        common_words = helper.most_common_words(selected_df, df)
        st.header('Most Common words')
        fig,ax = plt.subplots()
        ax.barh(common_words['word'],common_words['count'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji Analysis
        emoji_df = helper.helper_emoji(selected_df, df)
        st.title('Emoji Analysis')
        col1,col2 = st.columns(2)
        with col1:
            st.header('Most Emojis Used')
            st.dataframe(emoji_df)
        with col2:
            st.header('Pie Chart of Emojis')
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1],labels=emoji_df[0],startangle=90, autopct='%1.1f%%')
            ax.axis('equal')
            st.pyplot(fig)

        user_heatmap = helper.activity_heatmap(selected_df, df)
        st.title('Heatmap user')
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)





