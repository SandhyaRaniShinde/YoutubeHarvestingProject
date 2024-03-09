# Global Modules Import
import streamlit as st #web application
from pprint import pprint #pretty printing data structures
import json 

# Local Modules Import
from YoutubeHarvesting_Module.YoutubeScrapper import YoutubeScrapper
from YoutubeHarvesting_Module.MongoDBMigration import MongoDBMigration
from YoutubeHarvesting_Module.SQLDBMigration import SQLDBMigration
from YoutubeHarvesting_Module.SQLQuery import SQLQuery
from YoutubeHarvesting_Module.FetchMongoDB import FetchMongoDB

def main():

    # Initialize session state
    if 'youtube_channel_data' not in st.session_state:
        st.session_state.youtube_channel_data = {}

    #page configuration
    st.set_page_config(
        page_title="Youtube Data Harvesting Project",
        page_icon="👋",
    )
    #adds header
    st.markdown('# Youtube Data Harvesting Project')
    
    # Sidebar
    option = st.sidebar.radio("Select an Option", ["Fetch Channel Data", "Channel Name", "Migrate Channel data", "Query Data"])

    #option handling
    if option == "Fetch Channel Data":
        # Fetch Channel Data
        channel_id = st.sidebar.text_input('Enter the Youtube Channel Id')
        fetch_channel_data_button = st.sidebar.button('Fetch Channel Data')

        if fetch_channel_data_button:
            if channel_id:
                youtubescraper = YoutubeScrapper(channel_id)
                st.session_state.youtube_channel_data = youtubescraper.channel_data()
                #print("Youtube Channel Data:")
                #pprint(st.session_state.youtube_channel_data)

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

    if option == "Migrate Channel data":
        if st.button('Click here if you want to push the data'):
            mongodbmigration = MongoDBMigration(st.session_state.youtube_channel_data)
            st.session_state.youtube_channel_data = mongodbmigration.mongodbmigration()
            sqldbmigration = SQLDBMigration(st.session_state.youtube_channel_data)
            st.write(sqldbmigration.sqldbmigration())

    if option == "Query Data":
        query_option = st.selectbox(
        'Please select the query - ',
        ["1.What are the names of all the videos and their corresponding channels?",
         "2.Which channels have the most number of videos, and how many videos do they have?",
         "3.What are the top 10 most viewed videos and their respective channels?",
         "4.How many comments were made on each video, and what are their corresponding video names?",
         "5.Which videos have the highest number of likes, and what are their corresponding channel names?",
         "6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
         "7.What is the total number of views for each channel, and what are their corresponding channel names?",
         "8.What are the names of all the channels that have published videos in the year 2022?",
         "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?",
         "10.Which videos have the highest number of comments, and what are their corresponding channel names?",
        ],

        index=None,
        help="Select query to fetch the data")

        if query_option:
            sqlquerydata = SQLQuery(query_option)

            st.dataframe(sqlquerydata.sqlquery(), use_container_width=True)
    
    if option == "Channel Name":
        mongodbdata = FetchMongoDB()
        channel_name = mongodbdata.channel_name()

        query_option = st.selectbox(
        'Please select the Channel Name - ',
        channel_name,
        index=None,
        help="Select Channel Name to fetch the data"
        )
        if query_option:
            st.write(mongodbdata.fetchMongoDBData(query_option))
        
if __name__ == "__main__":
    main()