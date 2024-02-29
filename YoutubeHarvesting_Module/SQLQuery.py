# Global Modules Import
import mysql.connector
import pandas as pd

class SQLQuery:
    def __init__(self, Option) -> None:
        self.option = Option

    def sqlquery(self):
        connection = mysql.connector.connect(host="localhost",user="root",password="8686542162",database="youtubeDataHarvesting")
        #mycursor = connection.cursor()

        match self.option:
            case "1.What is the total number of views for each channel, and what are their corresponding channel names?":
                sql_query = """select distinct(channel_name) as channel_name, max(channel_views) as channel_views
                from channel 
                group by channel_name;"""
                #query_result = mycursor.execute(sql_query)
                df = pd.read_sql(sql_query, connection)
                return df
            case "2.What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
                sql_query = """SELECT  DISTINCT (video_name) AS 'Video Name', like_count AS 'Total Likes', dislike_count AS 'Total Dislikes'
                FROM video;"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "3.Which videos have the highest number of likes, and what are their corresponding channel names?":
                sql_query = """SELECT video.video_id, channel.channel_name, video.like_count 
                FROM video
                JOIN channel ON video.video_id = channel.channel_id
                WHERE video.like_count = (SELECT MAX(like_count) FROM video);"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "4.What are the names of all the videos and their corresponding channels?":
                sql_query = """select video_name, channel.channel_name
                from video, playlist, channel;"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "5.Which channel have the most number of videos, and how many videos do they have?":
                sql_query = """SELECT
                        channel.channel_id as ChannelId,
                        channel.channel_name as ChannelName,
                        COUNT(video.video_id) AS VideoCount
                    FROM
                        channel, playlist, video
                    GROUP BY
                        channel.channel_id, channel.channel_name
                    ORDER BY
                        VideoCount DESC
                    LIMIT 1;"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "6.What are the top 10 most viewed videos and their respective channels?":
                sql_query = """SELECT video.video_id,video.video_name,video.view_count,channel.channel_name 
                FROM video
                JOIN playlist ON video.playlist_id = playlist.playlist_id
                JOIN channel ON playlist.channel_id = channel.channel_id
                ORDER BY video.view_count DESC
                LIMIT 10;"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "7.How many comments were made on each video, and what are their corresponding video names?":
                sql_query = """SELECT video.video_id, video.video_name, COUNT(comment.comment_id) AS comment_count 
                FROM video
                LEFT JOIN comment ON video.video_id = comment.video_id
                GROUP BY video.video_id, video.video_name
                ORDER BY comment_count DESC;"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "8.What are the names of all the channels that have published videos in the year 2022?":
                sql_query = """SELECT DISTINCT channel.channel_name
                FROM channel
                JOIN playlist ON channel.channel_id = playlist.channel_id
                JOIN video ON playlist.playlist_id = video.playlist_id
                WHERE YEAR(video.publised_date) < 2022;"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?":
                sql_query = """SELECT channel.channel_name, AVG(video.duration) AS average_duration
                FROM channel
                JOIN playlist ON channel.channel_id = playlist.channel_id
                JOIN video ON playlist.playlist_id = video.playlist_id
                GROUP BY channel.channel_name
                ORDER BY average_duration DESC;"""
                df = pd.read_sql(sql_query, connection)
                return df
            case "10.Which videos have the highest number of comments, and what are their corresponding channel names?":
                sql_query = """SELECT video.video_id, video.video_name, COUNT(comment.comment_id) AS comment_count, channel.channel_name
                FROM video
                JOIN playlist ON video.playlist_id = playlist.playlist_id
                JOIN channel ON playlist.channel_id = channel.channel_id
                LEFT JOIN comment ON video.video_id = comment.video_id
                GROUP BY video.video_id, video.video_name, channel.channel_name
                ORDER BY comment_count DESC
                LIMIT 5;"""
                df = pd.read_sql(sql_query, connection)
                return df

