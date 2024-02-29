# Global Modules Import
import streamlit as st
from pprint import pprint
import json

# Local Modules Import
from YoutubeHarvesting_Module.YoutubeScrapper import YoutubeScrapper
from YoutubeHarvesting_Module.MongoDBMigration import MongoDBMigration
from YoutubeHarvesting_Module.SQLDBMigration import SQLDBMigration
from YoutubeHarvesting_Module.SQLQuery import SQLQuery

def main():
    # Initialize session state
    if 'youtube_channel_data' not in st.session_state:
        st.session_state.youtube_channel_data = {}

    st.set_page_config(
        page_title="Youtube Data Harvesting Project",
        page_icon="👋",
    )

    st.markdown("# Youtube Data Harvesting Project")
    
    # Sidebar
    option = st.sidebar.radio("Select an Option", ["Fetch Channel Data", "Migrate Channel data to MongoDB", "Migrate Channel data to SQLDB", "Query Data"])

    if option == "Fetch Channel Data":
        # Fetch Channel Data
        channel_id = st.sidebar.text_input('Enter the Youtube Channel Id')
        fetch_channel_data_button = st.sidebar.button('Fetch Channel Data')

        if fetch_channel_data_button:
            if channel_id:
                youtubescraper = YoutubeScrapper(channel_id)
                st.session_state.youtube_channel_data = youtubescraper.channel_data()
                print("Youtube Channel Data:")
                pprint(st.session_state.youtube_channel_data)

                # Create a download button

                json_str = json.dumps(st.session_state.youtube_channel_data)

                st.download_button(
                    "Download as json",
                    data=json_str,
                    file_name="output.json",
                    mime="application/json",
                )

                # Display the JSON data on the app
                st.json(st.session_state.youtube_channel_data)

            else:
                st.sidebar.warning("Please enter a valid Youtube Channel Id.")

    if option == "Migrate Channel data to MongoDB":
        if st.button('Click here if you want to push the data to MongoDB'):
            mongodbmigration = MongoDBMigration(st.session_state.youtube_channel_data)
            st.write(mongodbmigration.mongodbmigration())

    if option == "Migrate Channel data to SQLDB":
        if st.button('Click here if you want to push the data to SQLDB'):
            sqldbmigration = SQLDBMigration(st.session_state.youtube_channel_data)
            st.write(sqldbmigration.sqldbmigration())

    if option == "Query Data":
        query_option = st.selectbox(
        'Please select the query - ',
        ('1.What is the total number of views for each channel, and what are their corresponding channel names?', 
        '2.What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
        '3.Which videos have the highest number of likes, and what are their corresponding channel names?', 
        '4.What are the names of all the videos and their corresponding channels?',
        '5.Which channel have the most number of videos, and how many videos do they have?',
        '6.What are the top 10 most viewed videos and their respective channels?',
        '7.How many comments were made on each video, and what are their corresponding video names?',
        '8.What are the names of all the channels that have published videos in the year 2022?',
        '9.What is the average duration of all videos in each channel, and what are their corresponding channel names?',
        '10.Which videos have the highest number of comments, and what are their corresponding channel names?',
         ),

         index=None,
        placeholder="Select query...")

        if query_option:
            sqlquerydata = SQLQuery(query_option)

            st.dataframe(sqlquerydata.sqlquery(), use_container_width=True)
        

if __name__ == "__main__":
    main()
