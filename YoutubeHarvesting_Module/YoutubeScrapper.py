# Global Modules Import
from googleapiclient.discovery import build
from pprint import pprint
from collections import defaultdict

# Local Modules Import
from Utilities.APIStaticData import EnvironmentReader

class YoutubeScrapper:
    def __init__(self, channelId) -> None:
        self.channelId = channelId

    def channel_data(self):
        env_reader = EnvironmentReader()
        api_key = env_reader.get_specific_variable('GOOGLEAPIKEY')
        api_service_name = "youtube"
        api_version = "v3"
        channel_id = self.channelId

        #  # Get credentials and create an API client
        youtube = build(api_service_name, api_version, developerKey=api_key)

        # api hit-> endpoint channels.list
        channel_response = youtube.channels().list(
            id=channel_id,
            part='snippet,statistics,contentDetails,status'
        )

        # api channel.list execute
        channel_data = channel_response.execute()

        # get channel_information 
        channel_informations = {
            'channel_id' : channel_data['items'][0]['id'],
            'channel_name' : channel_data['items'][0]['snippet']['title'],
            'channel_description' : channel_data['items'][0]['snippet']['description'],
            #'playlists' : channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
            'total_video_count' : channel_data['items'][0]['statistics']['videoCount'],
            'total_view_count' : channel_data['items'][0]['statistics']['viewCount'],
            'total_subscriber_count' : channel_data['items'][0]['statistics']['subscriberCount'],
            'channel_status' : channel_data['items'][0]['status']['privacyStatus'] 
            if 'status' in channel_data['items'][0] else None,
            'channel_type' : channel_data['items'][0]['kind']
            if 'kind' in channel_data['items'][0] else None
            }
        
        #print("Channel_Informations")
        #pprint(channel_informations)

        # pull the playlists data to fetch the video ids
        playlist_request = youtube.playlists().list(
            part="snippet,contentDetails",
            channelId=channel_id,
            maxResults=25
        )

        playlist_data = playlist_request.execute()

        playlist_ids = []
 
        for i in playlist_data['items']:
            playlist_ids.append(i['id'])

        #print("playlist_ids")
        #pprint(playlist_ids)

        playlist_names = []

        for item in playlist_data['items']:
            playlist_names.append(item['snippet']['title'])

        #extract playlist_informaton
            
        playlist_information = {}

        for index,playlist in enumerate(playlist_data['items']):
            playlist_id = playlist['id']
            playlist_name = playlist['snippet']['title']
            playlist_key = "playlist_" + str(index)
            playlist_information[playlist_key] = {'playlist_id':playlist_id,'playlist_name':playlist_name,'channel_id':channel_id}

        #print("playlist_information")
        #pprint(playlist_information)


        # extract video_data
        # Hit the search endpoint on Channel id to fetch all videos id

        max_results = 50
        search_request = youtube.search().list(
            part='id',
            channelId=channel_id,
            maxResults=max_results
        )

        search_response = search_request.execute()

        #pprint(search_response)

        #extract video_ids
        video_ids = [item['id'].get('videoId') for item in search_response.get('items')]

        video_ids = list(dict.fromkeys(video_ids))
        try:
            video_ids.remove(None)
            
        except Exception as e:
                print(f"No None values in video ids")
            
        #pprint(video_ids)

        #extract video_information_list        

        playlist_videoid_mapping = defaultdict(list) ## {playlistid:videoid}

        for playlist_item in playlist_ids:
            playlistitems_request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_item,
            maxResults = 50
            )
            playlistitems_response = playlistitems_request.execute()


            totalResults = playlistitems_response.get('pageInfo').get('totalResults')

            for index in range(int(totalResults)):
                videoid = playlistitems_response.get('items')[index].get('snippet').get('resourceId').get('videoId')
                playlist_videoid_mapping[videoid].append(playlist_item)

        #pprint(playlist_videoid_mapping)

        # video Section
        video_information_list = {}

        # iterating over each video
        for index,video_id in enumerate(video_ids):
            try:
                video_response = youtube.videos().list(
                    part='snippet,statistics,contentDetails,status',
                    id=video_id
                ).execute()

                comment_request = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id
                )
                comments_response = comment_request.execute()

                if video_response and 'items' in video_response and video_response['items']:
                    key = 'video_information_' + str(index)
                    video_information_list.update({
                        key: [{
                            "playlist_id" : playlist_videoid_mapping.get(video_id, []),
                            "Video_Id": video_id,
                            "Video_Name": video_response['items'][0]['snippet']['title'] if 'title' in video_response['items'][0]['snippet'] else "Not Available",
                            "Video_Description": video_response['items'][0]['snippet']['description'],
                            "Likes": video_response['items'][0]['statistics']['likeCount'] if 'likeCount' in video_response['items'][0]['statistics'] else 0,
                            "Dislikes": video_response['items'][0]['statistics']['dislikeCount'] if 'dislikeCount' in video_response['items'][0]['statistics'] else 0,
                            "comment_count": video_response['items'][0]['statistics']['commentCount'] if 'commentCount' in video_response['items'][0]['statistics'] else 0,
                            "Shares": video_response['items'][0]['statistics']['shareCount'] if 'shareCount' in video_response['items'][0]['statistics'] else 0,
                            "view_count": video_response['items'][0]['statistics']['viewCount'],
                            "duration": video_response['items'][0]['contentDetails']['duration'],
                            "publised_date" : video_response['items'][0]['snippet']['publishedAt'],
                            "caption_status": 'Available' if 'captions' in video_response['items'][0]['contentDetails'] else 'Not Available',
                            "favorite_count": int(video_response['items'][0]['statistics']['favoriteCount']) if 'favoriteCount' in video_response['items'][0]['statistics'] else 0,
                            "thumbnail": video_response['items'][0]['snippet']['thumbnails']['default']['url'],

        
                        }]
                    })
                else:
                    print(f"No data found for video with ID: {video_id}")

                for index,comment in enumerate(comments_response['items']):
                    comment_key = 'comment_information_' + str(index)
                    video_information_list[key].append({
                        comment_key: {
                        "Comment_Id": comment['snippet']['topLevelComment']['id'],
                        "Comment_Text": comment['snippet']['topLevelComment']['snippet']['textDisplay'],
                        "Comment_Author": comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        "Comment_PublishedAt": comment['snippet']['topLevelComment']['snippet']['publishedAt']  
                        }
                    })

            except Exception as e:
                print(f"Error fetching data for video with ID {video_id}: {str(e)}") 

        # update the Video Information list with Channel Informations
        video_information_list.update(channel_informations)

        # update the Video Information list with playlist_information
        video_information_list.update(playlist_information)
        video_information_list.update({'playlist_count' : len(playlist_information)})

        return video_information_list