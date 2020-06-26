import praw
import json
import numpy as np
import pymongo
from praw.models import MoreComments
from pymongo import MongoClient
import pandas as pd


reddit = praw.Reddit(client_id='CWXzjQwNjI_FoA', client_secret="KJiUr5MHMdVW91L7IabUDEMaeIc",
                     password='Tbogtbog123', user_agent='USERAGENT',
                     username='ShayTann666')
reddit.subreddit('test').submit('Test Submission', url='https://reddit.com')
import datetime
#Partie Connection avec la DB

client = MongoClient('localhost',27017)
db = client['Comments_database'] #Definir la database
comment = db['api_comment'] #Definir la collection
topic = db['api_topic']
posts = []
blacklist = {"PresidentialRaceMemes",  #J'essaie d'eviter quelque reddit populaire qui ne sert pas a grande chose ( c'est des reddits pour rigoler ou bien )
    "comedyheaven",
    "pics",
    "memes",
    "videos",
    "nextfuckinglevel",
    "pcmasterrace",
    "BikiniBottomTwitter",
    "BlackPeopleTwitter",
    'porn',
    'meme',
    'comedy',
    'memes',
    'suck',
    'gifs',
    'fucking',
    'dank',
    'youseeingthisshit'
}

tmp_id = 0 #Pour savoir on est sur quelle reddit afin de tirer les commentaires proprement 
current_id = 0 #Pour les topics

ml_subreddit = reddit.subreddit('popular')
trending_reddit = ""
subreddit_trending = ""
topic_trending = ""
auteur_trending = ""
score_trending = ""
data = {}
f = open("D:\\Master MBD S2\\No-sql\\Projet\\NoSQL-Projet-master\\NoSQL-Projet-master\\Crawling\\index.txt", "r")
f2 = open("D:\\Master MBD S2\\No-sql\\Projet\\NoSQL-Projet-master\\NoSQL-Projet-master\\Crawling\\last_time.txt", "r")
index = int(f.read()) #c'est parce-que Django veut un ID int32 mais Mongo utilise un "_ID" de type ObjectId ce qui cause une erreur de manque field ID .., ce index "id" je ne vais jamais l'utiliser
print(index)

def getAll():
    global posts,auteur_trending
    for post in ml_subreddit.hot(limit=10):
        posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created,post.author])
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created','author'])

    

    
def getNext():
    global current_id,trending_reddit,score_trending,topic_trending,auteur_trending,subreddit_trending

    trending_reddit = posts.iloc[current_id]

    current_id += 1
    print(trending_reddit.subreddit)
    if trending_reddit.subreddit in blacklist:
        getNext()
    else : 
        if (check_if_string_in_file("D:\\Master MBD S2\\No-sql\\Projet\\NoSQL-Projet-master\\NoSQL-Projet-master\\Crawling\\subreddits.txt",str(trending_reddit.subreddit))):
            getNext() #Pour eviter de crawler toujours la même subreddit 
            
        else:
            
            topic_trending = trending_reddit.title  #C'est pas très utile puisque on va reverifier après . (c'est la difference entre trending topic dans populaire et dans son subreddit)
            subreddit_trending = trending_reddit.subreddit
            score_trending = int(trending_reddit.score)
            f3 = open("D:\\Master MBD S2\\No-sql\\Projet\\NoSQL-Projet-master\\NoSQL-Projet-master\\Crawling\\subreddits.txt", "a")
            auteur_trending = trending_reddit.author ## je sauvgarde le titre et l'auteur du topic pour organiser mes fichiers json après
            f3.write("\n"+str(subreddit_trending))
            f3.close()


def getPosts(): #On obtient toutes les sujets de tendances sur reddit
    global current_id,trending_reddit,f2,topic_trending,score_trending
    posting = []
    hot_posts = reddit.subreddit(str(trending_reddit.subreddit))
    # choosen_subreddit = reddit.subreddit(str(trending_reddit.subreddit))
    for post in hot_posts.hot(limit=10):
        
        posting.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posting = pd.DataFrame(posting,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    trending_reddit = posting.iloc[current_id]
    current_id += 1
    
    
    if (check_if_string_in_file("D:\\Master MBD S2\\No-sql\\Projet\\NoSQL-Projet-master\\NoSQL-Projet-master\\Crawling\\last_time.txt",str(trending_reddit.title))): #Si le topic est déja pris donc on passe au prochain topic
        getPosts()

    else :
        f2 = open("D:\\Master MBD S2\\No-sql\\Projet\\NoSQL-Projet-master\\NoSQL-Projet-master\\Crawling\\last_time.txt", "a") #Une fois avoir récuperer notre topic on vas l'enregistrer dans notre fichier text pour le prochain scrapping
        f2.write("\n"+str(trending_reddit.title))
        f2.close()
        topic_trending = trending_reddit.title
        score_trending = int(trending_reddit.score)
        



def getComments():
    global trending_reddit,index
    tableComs = []

    comsRed = reddit.submission(id=trending_reddit.id)
    for reply in comsRed.comments : 
        if isinstance(reply, MoreComments):
            continue #Pour eviter un erreur de library PRAW (cette technique est mentionner dans leurs site de documentation)
        tableComs.append([reply.author,reply.body,reply.score])
    tableComs = pd.DataFrame(tableComs,columns=['Auteur','Commentaire','Score'])

    
    for elm in tableComs.index : #Pour ecrire les commentaires directement dans la base de donnée

        data = {
            'id'     : index,
            'date'   : datetime.datetime.now(),
            'author' : str(tableComs['Auteur'][elm]),
            'body'   : str(tableComs['Commentaire'][elm]),
            'score'  : int(tableComs['Score'][elm]),
            'topic'  : trending_reddit.title
        }
        index += 1
        data = correct_encoding(data) 
        comment.insert_one(data)

def correct_encoding(dictionary):  #Pour corriger l'erreur de type var numpy.int64
    new = {}
    for key1, val1 in dictionary.items():
        # Nested dictionaries
        if isinstance(val1, dict):
            val1 = correct_encoding(val1)

        if isinstance(val1, np.bool_):
            val1 = bool(val1)

        if isinstance(val1, np.int64):
            val1 = int(val1)

        if isinstance(val1, np.float64):
            val1 = float(val1)

        new[key1] = val1

    return new

def check_if_string_in_file(file_name, string_to_search): #Pour vérifier dans notre fichier text last_one s'il on a deja pris ce topic ou pas
    
   
    with open(file_name, 'r') as read_obj:
       
        for line in read_obj:
            # On parcourir line par line et on verifie s'il contient notre string
            if string_to_search in line:
                return True
    return False

if __name__ == "__main__":
    getAll()
    getNext()
    current_id = 0
    getPosts()
    data = {
        'id'     : index, #Ce field est pour éviter l'erreur "No field ID " dans Django je vais pas utiliser cette variable
        'date'   : datetime.datetime.now(),
        'author' : str(auteur_trending),
        'body'   : topic_trending,
        'score'  : int(score_trending),
        'subreddit' : str(subreddit_trending),
        'number_comments' : 0,
        'positivity' : 0,
        'negativity' : 0,
        'clustering1' : "",
        'clustering2' : ""
    }
    index += 1
    data = correct_encoding(data)
    topic.insert_one(data) #On insert dans notre base de donnée le topic
    getComments()
    client.close #on ferme l'instance de la database
    topic.close
    f = open("D:\\Master MBD S2\\No-sql\\Projet\\NoSQL-Projet-master\\NoSQL-Projet-master\\Crawling\\index.txt", "w")
    f.write(str(index)) #J'ècrit mon index que j'ai incrémenter dans le même fichier " overwrite " pour l'utiliser quand je relance le script
    f.close()