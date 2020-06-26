import praw
import json
from datetime import datetime
from praw.models import MoreComments
import pandas as pd
reddit = praw.Reddit(client_id='CWXzjQwNjI_FoA', client_secret="KJiUr5MHMdVW91L7IabUDEMaeIc",
                     password='Tbogtbog123', user_agent='USERAGENT',
                     username='ShayTann666')
reddit.subreddit('test').submit('Test Submission', url='https://reddit.com')





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
ml_subreddit = reddit.subreddit('popular')
trending_reddit = ""
topic_trending = ""
auteur_trending = ""
score_trending = ""
data = {}

def getAll():
    global posts,auteur_trending
    for post in ml_subreddit.hot(limit=10):
        posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created,post.author])
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created','author'])
    print(posts)
    

    
def getNext():
    global current_id,ml_subreddit,reddit,trending_reddit,score_trending,topic_trending,auteur_trending
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
        else : 
            getNext() #En cas on a un topic avec un mot interdit on vas passé les operations en haut et on vas directement passé à l'autre topic



def getPosts(): #On obtient toutes les sujets de tendances sur reddit
    posting = []
    hot_posts = reddit.subreddit(str(trending_reddit.subreddit))
    # choosen_subreddit = reddit.subreddit(str(trending_reddit.subreddit))
    for post in hot_posts.hot(limit=10):
        posting.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posting = pd.DataFrame(posting,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    print(posting)   #J'affiche les 10 tops sujets    


def getComments():
    global trending_reddit
    tableComs = []
    comsRed = reddit.submission(id=trending_reddit.id)
    for reply in comsRed.comments : 
        if isinstance(reply, MoreComments):
            continue #Pour eviter un erreur de library PRAW (cette technique est mentionner dans leurs site de documentation)
        tableComs.append([reply.author,reply.body,reply.score])
    tableComs = pd.DataFrame(tableComs,columns=['Auteur','Commentaire','Score'])
    print(tableComs)
    
    for elm in tableComs.index : #Pour ecrire les commentaires dans un fichier json
    #     data['Topic'].append({ #Pour chaque commentaire on ajoute le sujet pour bien structuré nos données même si de la repitition mais sa sera utile dans le cas où on traite chaque commentaire de façon individuel
    #     'auteur' : str(auteur_trending),
    #     'body'   : topic_trending,
    #     'score'  : score_trending,
    # })
        data['comments'].append({
            'author' : str(tableComs['Auteur'][elm]),
            'body'   : str(tableComs['Commentaire'][elm]),
            'score'  : str(tableComs['Score'][elm]),
        })



if __name__ == "__main__":
    getAll()
    getNext()
    current_id = 0
    print("You've choosen :"+str(trending_reddit.subreddit))
    input("Press any key to continue into Trending topics on your Subredit")
    getPosts()
    # data['Topic'] = []
    data['comments'] = []  # initialiser la balise commentaire dans notre fichier json
    data['comments'].append({  #Dans une première version je note qu'une seule fois le sujet et son auteur mais après j'ai changer d'avis je la note dans chaque commentaire
        'auteur' : str(auteur_trending),
        'body'   : topic_trending,
        'score'  : score_trending
    })
    input ("Press any key to get comments ")
    getComments()
    now = datetime.now()
    current_time = now.strftime("%H_%M")
    df = pd.DataFrame.from_dict(data, orient='index') #On stock tout dans une DataFrame "la puissance de panda "
  
    df.transpose()
    print(df)
    df.dropna() # On supprime les lignes qui ont des données manquant 
    df.to_json(str(current_time)+'_data.json') #Sauvgarde dans un document json 
    # with open(str(current_time)+'_data.json', 'w',encoding='utf8') as outfile:      #Si on veut les sauvgarder sans utiliser panda
    #     json.dump(data, outfile,ensure_ascii=False)
