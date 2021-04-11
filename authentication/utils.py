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

class SessionHandle():
    def __init__(self,request):
        self.session = request.session
        usersession = self.session.get('userinfo')
        if 'userinfo' not in request.session:
            usersession = self.session['userinfo'] = {}
        self.usersession = usersession

    def add(self,sessionobject):
        """
        Adding or Updating User Session

        """
        self.usersession = sessionobject
        
        self.save()

    def __len__(self):
        return len(self.usersession)        

    def clear(self):
        for _ in self.session.keys():
            del self.session[_]
        self.save()


    def save(self):
        self.session.modified = True


# SECRET_KEY = '&po3&kr8dbje7m-d^yi%5jdu0+go@i^51_*4yy_1u-n6qxr2%i'
# EMAIL_HOST_USER = 'nagendumar@ymail.com'
# EMAIL_HOST_PASSWORD = 'hfhbijolsbordwmk'
# dbpwd = 'k#8Ned!Xak9KFgsbtC'