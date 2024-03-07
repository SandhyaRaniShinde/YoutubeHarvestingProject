# Global Modules Import
import mysql.connector
import pandas as pd
from Utilities.APIStaticData import EnvironmentReader

class SQLQuery:
    def __init__(self, Option) -> None:
        self.option = Option

    def sqlquery(self):
        env_reader = EnvironmentReader()
        server_pass = env_reader.get_specific_variable('SERVERPASS')
        connection = mysql.connector.connect(host="localhost",user="root",password=server_pass,database="youtubeDataHarvesting")
        #mycursor = connection.cursor()

        match self.option:
            case "1.What are the names of all the videos and their corresponding channels?":
                sql_query = """SELECT c.channel_name,v.video_name
                from channel AS C Join video AS v on c.channel_id = v.channel_id;"""
                #query_result = mycursor.execute(sql_query)
                df = pd.read_sql(sql_query, connection)
                return df
            case "2.Which channels have the most number of videos, and how many videos do they have?":
                sql_query = """SELECT channel.channel_id as ChannelId,
                        channel.channel_name as ChannelName,
                        COUNT(video.video_id) AS VideoCount
                    FROM
                        channel, video
                    GROUP BY
                        channel.channel_id, channel.channel_name
                    ORDER BY
                        VideoCount DESC
                    LIMIT 1;"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "3.What are the top 10 most viewed videos and their respective channels?":
                sql_query = """SELECT v.video_name, c.channel_name, v.view_count
                FROM video v
                JOIN  channel c ON v.channel_id = c.channel_id
                ORDER BY v.view_count DESC
                LIMIT 10;"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "4.How many comments were made on each video, and what are their corresponding video names?":
                sql_query = """select video_id,video_name,comment_count from video
                order by comment_count DESC;"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "5.Which videos have the highest number of likes, and what are their corresponding channel names?":
                sql_query = """SELECT distinct(V.video_id),C.channel_name,v.like_count
                from channel AS C Join video AS v on c.channel_id = v.channel_id
                ORDER BY like_count DESC;"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
                sql_query = """SELECT  DISTINCT (video_name) AS 'Video Name', like_count AS 'Total Likes', dislike_count AS 'Total Dislikes'
                FROM video;"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "7.What is the total number of views for each channel, and what are their corresponding channel names?":
                sql_query = """select distinct(channel_name) as channel_name, max(channel_views) as channel_views
                from channel 
                group by channel_name;"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "8.What are the names of all the channels that have published videos in the year 2022?":
                sql_query = """select * from video where publised_date > '2022-01-01 00:00:00'AND publised_date < '2023-01-01 00:00:00';"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?":
                sql_query = """SELECT (channel.channel_name), AVG(video.duration) AS average_duration
                FROM video
                JOIN channel ON channel.channel_id = video.channel_id
                GROUP BY channel_name
                ORDER BY average_duration DESC;"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "10.Which videos have the highest number of comments, and what are their corresponding channel names?":
                sql_query = """SELECT channel_id AS Channel_id,video_id AS Video_ID,comment_count AS Comments
                            FROM video
                            ORDER BY Comments DESC
                            LIMIT 10"""
                df = pd.read_sql(sql_query, connection)
                return df

