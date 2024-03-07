# Global Modules Import
from pymongo import MongoClient

# Local Modules Import
from Utilities.APIStaticData import EnvironmentReader

class MongoDBMigration:
    def __init__(self, channel_data) -> None:
        self.channel_data = channel_data
    
    def mongodbmigration(self):
        try:
            env_reader = EnvironmentReader()
            server_pass = env_reader.get_specific_variable('SERVERPASS')
            connection = MongoClient(f"mongodb+srv://sandhyaranishinde:{server_pass}@cluster0.vu6kqnp.mongodb.net/")
            db = connection['YoutubeDataHarvesting_Project1']
            element = db['channel_information']
            element.insert_one(self.channel_data)
            latest_document = element.find_one({}, sort=[("_id", -1)])
            return latest_document
        except Exception as e:
            return f"Error Migrating data to Mongo DB: {str(e)}"