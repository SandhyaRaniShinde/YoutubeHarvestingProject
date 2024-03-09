 Youtube Data Harvesting Project in Python

Overview 
    This Python project is designed to harvest data from YouTube, including information about channels, playlists, videos, and comments. It provides functionalities for fetching data, migrating it to MongoDB and SQL databases, and executing SQL queries on the migrated data.

 Project Structure
   The project follows a modular structure for better organization and maintainability:

Table of Contents
 YoutubeHarvestingProject
 ->main.py
 -->YoutubeHarvesting_Module
    --->YoutubeScrapper.py
    --->FetchMongoDB.py
    --->MongoDBMigration.py
    --->SQLDBMigration.py
    --->SQLQuery.py
---->Utilities
    ---->APIStaticData.py

Goal
Our goal is to create a comprehensive tool for harvesting and analyzing data from YouTube channels. By utilizing the YouTube API, our project aims to provide insights into channel statistics, video details, and comments. The modular structure allows for seamless migration of harvested data to databases like MongoDB and SQL, empowering users to perform advanced queries and visualizations. We aspire to offer a user-friendly and extensible solution for anyone interested in exploring and understanding YouTube data.

Guide
->main.py
     Module named "API static module" that includes the "os" module for interacting with the operating system. It defines a class called "EnvironmentReader" with a constructor that does nothing. The class has a method named "get_specific_variable" which takes a variable name as a parameter and retrieves its value from the environment using the "os.environ.get" method. This class can be used to read specific environment variables.

     -->YoutubeHarvesting_Module
        --->YoutubeScrapper.py
              class called "YoutubeScrapper" that uses the YouTube Data API to fetch information about a specified YouTube channel. It initializes with a channel ID and includes methods to extract details about the channel, its videos, and associated playlists. The class utilizes the "googleapiclient" library and an "EnvironmentReader" class to access sensitive API key information. The output is a concise dictionary containing comprehensive data, including channel details, video statistics, comments, and playlist information.
        
        --->FetchMongoDB.py
            The Python code, "FetchMongoDB," is designed to fetch channel names from a MongoDB database. It utilizes the "pymongo" library to establish a connection and interact with the database. The class initializes with credentials obtained from an "EnvironmentReader" class. The methods include "channel_name," which retrieves and prints channel names from the MongoDB collection, and "fetchMongoDBData," which fetches the latest document for a specific channel name from the collection. The code provides a straightforward approach to access and retrieve channel information stored in a MongoDB database.

        --->MongoDBMigration.py
            The "MongoDBMigration" class is a Python script designed to migrate YouTube channel data to a MongoDB database. It establishes a connection to the database, inserts the provided channel data into the 'channel_information' collection, and returns the latest document from the collection. If any errors occur during the migration, an error message is returned. This class simplifies the process of transferring YouTube channel information to MongoDB.

        --->SQLDBMigration.py
            The code defines a class, "SQLDBMigration," for efficiently migrating YouTube channel data, including videos and comments, to a MySQL database. It leverages input channel data, establishes a MySQL connection using environment credentials, and executes SQL queries to insert relevant information into respective tables. This migration covers channel details, playlists, videos, and associated comments. The code handles diverse data types, such as video statistics and comment details, seamlessly inserting them into the corresponding MySQL tables. The method "sqldbmigration" succinctly executes the migration process. Overall, this script streamlines the transfer of YouTube channel data to a structured MySQL database for improved management and analysis.

        --->SQLQuery.py
            The Python code features a class, "SQLQuery," that connects to a MySQL database storing YouTube channel data. It executes diverse SQL queries, each addressing specific insights such as video details, channel statistics, and user engagement. The queries cover a range of scenarios, providing concise results presented in Pandas dataframes. The modular structure facilitates quick access to information like video-channel relationships, popular videos, and channel statistics with minimal code complexity.



