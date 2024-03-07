# Global Modules Import
from pymongo import MongoClient

class MongoDBMigration:
    def __init__(self, channel_data) -> None:
        self.channel_data = channel_data
    
    def mongodbmigration(self):
        try:
            connection = MongoClient("mongodb+srv://sandhyaranishinde:8686542162@cluster0.vu6kqnp.mongodb.net/")
            db = connection['YoutubeDataHarvesting_Project1']
            element = db['channel_information']
            element.insert_one(self.channel_data)
            latest_document = element.find_one({}, sort=[("_id", -1)])
            return latest_document
        except Exception as e:
            return f"Error Migrating data to Mongo DB: {str(e)}"