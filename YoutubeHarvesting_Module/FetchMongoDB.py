# Global Modules Import
from pymongo import MongoClient
from Utilities.APIStaticData import EnvironmentReader

class FetchMongoDB:

    def __init__(self) -> None:
        env_reader = EnvironmentReader()
        server_pass = env_reader.get_specific_variable('serverpass')
        self.connection = MongoClient(f"mongodb+srv://sandhyaranishinde:{server_pass}@cluster0.vu6kqnp.mongodb.net/")
        self.db = self.connection['YoutubeDataHarvesting_Project1']
        self.element = self.db['channel_information']

    def channel_name(self):
        channel_name = {}

        for data in self.element.find():
            try:
                print(data['channel_name'])
                channel_name[data['channel_name']] = 1
            except Exception as e:
                print(f"Error fetching data from Mongo DB: {str(e)}")
        return channel_name.keys()
    
    def fetchMongoDBData(self, channelName):
        channel_doc = self.element.find_one({"channel_name": channelName}, sort=[("_id", -1)])
        self.connection.close()
        return channel_doc

        

        
        