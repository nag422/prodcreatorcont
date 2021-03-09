import pymongo
from pymongo import MongoClient
from django.conf import settings
conn=MongoClient(settings.MONGO_URL)
mongoconn=conn.reactreduxnode


class DatabaseDynamic():
    def __init__(self,request):
        self.user = request.user

    def insertrecordtodb(self,catname,thisdict):
        try:
            
            db = mongoconn
            colname=db[catname]              
            x = colname.insert_one(thisdict)
            bsonid = str(x.inserted_id)
            return bsonid
        except Exception as e:
            print(e)
            return e