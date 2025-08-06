import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: #3D5A80;'>📊 WhatsApp Chat Analyzer</h1>", unsafe_allow_html=True)
st.markdown("---")

st.sidebar.title("📁 Upload Chat File")
uploaded_file = st.sidebar.file_uploader("Choose your WhatsApp exported `.txt` file")

if uploaded_file is not None:
    data = uploaded_file.getvalue().decode("utf-8")
    df = preprocessor.preprocess(data)

    # user list for selection
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("📌 Select User", user_list)

    if st.sidebar.button("📈 Show Analysis"):

        # --- Top Stats ---
        st.markdown("## 🚀 Overall Stats")
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💬 Messages", num_messages)
        col2.metric("📝 Words", words)
        col3.metric("📷 Media Shared", num_media_messages)
        col4.metric("🔗 Links Shared", num_links)
        st.markdown("---")

        # --- Monthly Timeline ---
        with st.expander("📆 Monthly Timeline", expanded=True):
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='#3D5A80')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)

        # --- Daily Timeline ---
        with st.expander("📅 Daily Timeline"):
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#293241')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)

        # --- Activity Maps ---
        st.markdown("## 🗺️ Weekly & Monthly Activity")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📌 Most Active Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='#EE6C4D')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.markdown("### 🗓️ Most Active Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='#98C1D9')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # --- Weekly Activity Heatmap ---
        st.markdown("### 🔥 Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        if user_heatmap.empty:
            st.warning("Not enough data to generate the heatmap.")
        else:
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, cmap="YlGnBu", ax=ax)
            st.pyplot(fig)

        # --- Busiest Users ---
        if selected_user == 'Overall':
            st.markdown("## 👥 Most Active Users")
            x, new_df = helper.most_busy_users(df)
            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='#E0FBFC')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # --- WordCloud ---
        st.markdown("## ☁️ WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis('off')
        st.pyplot(fig)

        # --- Most Common Words ---
        st.markdown("## 🏆 Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='#3D5A80')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # --- Emoji Analysis ---
        st.markdown("## 😂 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            if not emoji_df.empty:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f", startangle=90)
                ax.axis('equal')
                st.pyplot(fig)
            else:
                st.write("No emojis found!")

        # --- Hourly Activity ---
        st.markdown("## ⏰ Most Active Hour")
        hourly_activity = helper.most_active_hour(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(hourly_activity.index, hourly_activity.values, color='#EE6C4D')
        ax.set_xticks(range(0, 24))
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Message Count")
        st.pyplot(fig)

        # --- Sentiment Analysis ---
        st.markdown("## ❤️ Sentiment Analysis")
        sentiments = helper.sentiment_analysis(selected_user, df)

        col1, col2 = st.columns(2)
        with col1:
            st.write("### Sentiment Distribution")
            sentiment_df = pd.DataFrame.from_dict(sentiments, orient='index').reset_index()
            sentiment_df.columns = ['Sentiment', 'Count']
            st.dataframe(sentiment_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(sentiments.values(), labels=sentiments.keys(), autopct='%0.2f', startangle=140)
            ax.axis('equal')
            st.pyplot(fig)
