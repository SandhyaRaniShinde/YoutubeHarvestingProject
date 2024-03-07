# Global Modules Import
import time
import mysql.connector
from datetime import datetime
import isodate


class SQLDBMigration:
    def __init__(self, channel_data) -> None:
        self.video_information_list = channel_data
    
    def sqldbmigration(self):
        connection = mysql.connector.connect(host="localhost",user="root",password="8686542162",database="youtubeDataHarvesting")
        mycursor = connection.cursor()
        video_information_list = self.video_information_list
        
        # Insert query for channel Table
        channel_query = "insert into channel(channel_id,channel_name,channel_type,channel_views,channel_description,channel_status) values(%s,%s,%s,%s,%s,%s)"
        channel_data = [
                (video_information_list["channel_id"],video_information_list["channel_name"],video_information_list["channel_type"],video_information_list["total_view_count"],video_information_list["channel_description"],video_information_list["channel_status"])
            ]
        mycursor.executemany(channel_query,channel_data)
        connection.commit()        

   
        # Insert query for Playlist Table

        for index,playlist in enumerate(range(int(video_information_list['playlist_count']))):
            try:
                getplaylist = "playlist_" + str(index)
                playlist_id = str(video_information_list[getplaylist]['playlist_id'])
                playlist_name = video_information_list[getplaylist]['playlist_name']
                channel_id = video_information_list['channel_id']


                playlist_query = "insert into Playlist(playlist_id, channel_id, playlist_name) values(%s,%s,%s)"
                playlist_data = [
                        (playlist_id,channel_id,playlist_name)
                    ]
                mycursor.executemany(playlist_query,playlist_data)
                connection.commit()

            except Exception as e:
                print(f"Error fetching data for playlist with ID {playlist_id}: {str(e)}")

        # Insert Query for Video Table


        for index,video in enumerate(range(int(video_information_list['total_video_count']))):
            try:
                date_format = "%Y-%m-%dT%H:%M:%SZ"
                getvideo = "video_information_" + str(index)
                Video_Id = (video_information_list[getvideo][0]['Video_Id'])
                Video_Name = (video_information_list[getvideo][0]['Video_Name'])
                Likes = int(video_information_list[getvideo][0]['Likes'])
                Dislikes = int(video_information_list[getvideo][0]['Dislikes'])
                Video_Description = (video_information_list[getvideo][0]['Video_Description'])
                comment_count = int(video_information_list[getvideo][0]['comment_count'])
                published_date = datetime.strptime(video_information_list[getvideo][0]['publised_date'], date_format)
                view_count = (video_information_list[getvideo][0]['view_count'])
                favorite_count = (video_information_list[getvideo][0]['favorite_count'])
                duration = int(isodate.parse_duration(video_information_list[getvideo][0]['duration']).total_seconds())
                thumbnail = str(video_information_list[getvideo][0]['thumbnail'])
                caption_status = str(video_information_list[getvideo][0]['caption_status'])
                playlist_id = video_information_list[getvideo][0]['playlist_id']
                playlist_id_str =  str(playlist_id) #', '.join(map(str, playlist_id))
                channel_id = video_information_list['channel_id']

                video_sql_query = "insert into video(video_id, playlist_id, video_name, video_description, publised_date, view_count, like_count, dislike_count, favorite_count, comment_count, duration, thumbnail, caption_status, channel_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                video_sql_data = [
                (Video_Id, playlist_id_str, Video_Name, Video_Description, published_date, view_count, Likes, Dislikes, favorite_count, comment_count, duration, thumbnail, caption_status,channel_id )
                ]

                mycursor.executemany(video_sql_query,video_sql_data)
                connection.commit()

            except Exception as e:
                print(f"Error fetching data for video with ID {Video_Id}: {str(e)}")

        ## comment data for SQL
        # Assuming 'total_video_count' is the key that stores the total number of videos
        total_video_count = int(video_information_list.get('total_video_count', 0))

        for video_index in range(total_video_count):
            try:
                date_format = "%Y-%m-%dT%H:%M:%SZ"
                video_key = 'video_information_' + str(video_index)
                comments = video_information_list.get(video_key, [])
                video_id = video_information_list.get(video_key, [])[0].get('Video_Id', 'Unknown')
                

                for comment_data in comments[1:]:
                    for comment_key, comment_info in comment_data.items():
                        comment_id = comment_info['Comment_Id']
                        comment_author = comment_info['Comment_Author']
                        comment_published_at = datetime.strptime(comment_info['Comment_PublishedAt'], date_format)
                        comment_text = comment_info['Comment_Text']

                        # insert the comment data into sql
                        comment_sql_query = "insert into Comment(comment_id, video_id, comment_text, comment_author, comment_published_date) values(%s,%s,%s,%s,%s)"
                        comment_sql_data = [
                        (comment_id, video_id, comment_text, comment_author, comment_published_at)
                        ]

                        mycursor.executemany(comment_sql_query,comment_sql_data)
                        connection.commit()

            except Exception as e:
                print(f"Error fetching comments data for video with index {video_id}: {str(e)}")
        
        return "Channel data is migrated."