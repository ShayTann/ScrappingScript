#Used to clean the old data (24h)

import pymongo
from pymongo import MongoClient
import datetime




time_now = datetime.datetime.now()
client = MongoClient('localhost',27017)
db = client['Comments_database'] #Definir la database
comment = db['api_comment'] #Definir la collection
topic = db['api_topic']

Topics = topic.find({})
Comments = comment.find({})

for doc in Topics : 
    date_time = doc['date']
    interv = time_now - date_time

    if (0 < int(str(interv)[0])):
        myquery = { "id": doc['id'] }
        topic.delete_one(myquery)
        file = "D:\\Master MBD S2\\No-sql\\Projet\\NoSQL-Projet-master\\NoSQL-Projet-master\\Crawling\\subreddits.txt"
        with open (file,'w') as clean:
            clean.write('')


for doc in Comments : 
    date_time = doc['date']
    interv = time_now - date_time
    if (0 < int(str(interv)[0])):
        myquery = { "id": doc['id'] }
        comment.delete_one(myquery)
        
topic.close
comment.close
client.close