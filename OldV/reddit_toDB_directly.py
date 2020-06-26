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

#Partie Connection avec la DB

client = MongoClient('localhost',27017)
db = client['Comments_database']
comment = db['api_comment']
topic = db['api_topic']
posts = []
blacklist = {"PresidentialRaceMemes",  #J'essaie d'eviter quelque reddit populaire qui ne sert pas a grande chose ( c'est des reddits pour rigoler )
    "comedyheaven",
    "pics",
    "memes",
    "videos",
    "nextfuckinglevel",
    "pcmasterrace",
    "BikiniBottomTwitter",
    "BlackPeopleTwitter"
}
switch_words = { #Là j'essaie d'eviter quelque mots , si ses mots se trouve dans le titre du reddit 100% des informations inutile pour notre projet
    'porn',
    'meme',
    'comedy',
    'memes',
    'suck',
    'gifs',
    'fucking',
    'dank'
}
current_id = 0
posting =""
ml_subreddit = reddit.subreddit('popular')
trending_reddit = ""
subreddit_trending = ""
topic_trending = ""
auteur_trending = ""
score_trending = ""
data = {}
f = open("C:/Users/Asus R.O.G/OneDrive/Master MBD S2/NoSql/Projet/Code/Crawling/index.txt", "r")

index = int(f.read()) #c'est parce-que Django veut un ID int32 mais Mongo utilise un "_ID" de type ObjectId ce qui cause une erreur de manque field ID .., ce index "id" je ne vais jamais l'utiliser


def getAll():
    global posts,auteur_trending
    for post in ml_subreddit.hot(limit=10):
        posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created,post.author])
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created','author'])
    print(posts)
    

    
def getNext():
    global current_id,ml_subreddit,reddit,trending_reddit,score_trending,topic_trending,auteur_trending,subreddit_trending
    print("Voyons voirr hmmmmmmmm : "+str(current_id))
    trending_reddit = posts.iloc[current_id]
    current_id += 1
    if trending_reddit.subreddit in blacklist:
        getNext()
    else : 
        statut = True
        for word in switch_words:
            if str(trending_reddit.subreddit).lower().find(word) != -1: # C'est le cas où un mots de nos mots interdit se trouve dans le titre
                statut = False                             #C'est à dire je vais prendre le prochaine reddit
        if statut : #Le cas où on a un sujet propre :
            choix = input ("The trending reddit is "+str(trending_reddit.subreddit)+" enter 1 to continue or 2 to pass into the next reddit or 3 to choose by id \n")
            topic_trending = trending_reddit.title
            subreddit_trending = trending_reddit.subreddit
            score_trending = trending_reddit.score
            auteur_trending = trending_reddit.author ## je sauvgarde le titre et l'auteur du topic pour organiser mes fichiers json après
            if (choix == "1"):
                print("The topic is : "+str(topic_trending)+" By : "+str(auteur_trending))
            if (choix == "2" ):
                getNext()
            if (choix == "3" ): 
                id_reddit = input ("Enter the ID of subreddit please ")
                trending_reddit = posts.loc[posts['id'] == id_reddit]
                topic_trending = trending_reddit.title
                auteur_trending = trending_reddit.author
                subreddit_trending = trending_reddit.subreddit
        else : 
            getNext() #En cas on a un topic avec un mot interdit on vas passé les operations en haut et on vas directement passé à l'autre topic



def getPosts(): #On obtient toutes les sujets de tendances sur reddit
    global posting
    posting = []
    hot_posts = reddit.subreddit(str(trending_reddit.subreddit))
    # choosen_subreddit = reddit.subreddit(str(trending_reddit.subreddit))
    for post in hot_posts.hot(limit=10):
        posting.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posting = pd.DataFrame(posting,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    print(posting)   #J'affiche les 10 tops sujets    


def getComments():
    global trending_reddit,index
    tableComs = []
    comsRed = reddit.submission(id=posts.iloc[current_id-1]['id'])
    print("Here !! : "+str(posts.iloc[current_id-1]['id']))
    print("c'etait "+str (current_id-1))
    for reply in comsRed.comments : 
        if isinstance(reply, MoreComments):
            continue #Pour eviter un erreur de library PRAW (cette technique est mentionner dans leurs site de documentation)
        tableComs.append([reply.author,reply.body,reply.score])
    tableComs = pd.DataFrame(tableComs,columns=['Auteur','Commentaire','Score'])
    print(tableComs)
    
    for elm in tableComs.index : #Pour ecrire les commentaires directement dans la base de donnée

        data = {
            'id'     : index,
            'author' : str(tableComs['Auteur'][elm]),
            'body'   : str(tableComs['Commentaire'][elm]),
            'score'  : str(tableComs['Score'][elm]),
            'topic'  : topic_trending
        }
        index += 1
        data = correct_encoding(data) #Pour corriger l'erreur de type var numpy.int64
        comment.insert_one(data)
def correct_encoding(dictionary):
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


if __name__ == "__main__":
    getAll()
    getNext()
    
    print("You've choosen :"+str(trending_reddit.subreddit))
    input("Press any key to continue into Trending topics on your Subredit")
    getPosts()
    data = {
        'id'     : index, #Ce field est pour éviter l'erreur "No field ID " dans Django je vais pas utiliser cette variable
        'author' : str(auteur_trending),
        'body'   : topic_trending,
        'score'  : score_trending,
        'subreddit' : str(subreddit_trending)
    }
    index += 1
    data = correct_encoding(data)
    topic.insert_one(data)
    input ("Press any key to get comments ")
    getComments()
    client.close
    topic.close
    f = open("C:/Users/Asus R.O.G/OneDrive/Master MBD S2/NoSql/Projet/Code/Crawling/index.txt", "w")
    f.write(str(index)) #J'ècrit mon index que j'ai incrémenter dans le même fichier " overwrite " pour l'utiliser quand je relance le script
    f.close()