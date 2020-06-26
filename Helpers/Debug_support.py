import pymongo
from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client['Comments_database'] #Definir la database
Support = db['api_supportevolution']
f = open("Crawling\index.txt", "r")
index = int(f.read())
data = [
    {'id' : index+19,
    'hour' : "0",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+20,
    'hour' : "1",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+21,
    'hour' : "2",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+22,
    'hour' : "3",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+23,
    'hour' : "4",
    'positivity' : 0,
    'negativity' : 0
},
    {'id' : index,
    'hour' : "5",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+1,
    'hour' : "6",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+2,
    'hour' : "7",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+3,
    'hour' : "8",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+4,
    'hour' : "9",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+5,
    'hour' : "10",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+6,
    'hour' : "11",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+7,
    'hour' : "12",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+8,
    'hour' : "13",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+9,
    'hour' : "14",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+10,
    'hour' : "15",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+11,
    'hour' : "16",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+12,
    'hour' : "17",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+13,
    'hour' : "18",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+14,
    'hour' : "19",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+15,
    'hour' : "20",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+16,
    'hour' : "21",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+17,
    'hour' : "22",
    'positivity' : 0,
    'negativity' : 0
},
{'id' : index+18,
    'hour' : "23",
    'positivity' : 0,
    'negativity' : 0
}
]
index += 1 
f = open("Crawling\index.txt", "w")
f.write(str(index))
Support.insert_many(data)
Support.close
client.close