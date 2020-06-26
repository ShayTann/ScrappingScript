import praw
import xlsxwriter 
from praw.models import MoreComments
import pandas as pd
reddit = praw.Reddit(client_id='CWXzjQwNjI_FoA', client_secret="KJiUr5MHMdVW91L7IabUDEMaeIc",
                     password='Tbogtbog123', user_agent='USERAGENT',
                     username='ShayTann666')
reddit.subreddit('test').submit('Test Submission', url='https://reddit.com')
# hot_posts = reddit.subreddit('MachineLearning').hot(limit=10)
# for post in hot_posts:
#     print(post.title)
posts = []
current_id = 0
ml_subreddit = reddit.subreddit('popular')
trending_reddit = ""
topic_trending = ""
row = 0
def getAll():
    global posts
    for post in ml_subreddit.hot(limit=10):
        posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    print(posts)
    
def getNext():
    global current_id,ml_subreddit,reddit,trending_reddit,topic_trending
    trending_reddit = posts.iloc[current_id]
    current_id += 1
    choix = input ("The trending reddit is "+str(trending_reddit.subreddit)+" enter 1 to continue or 2 to pass into the next reddit or 3 to choose by id \n")
    print(trending_reddit.title)
    topic_trending = trending_reddit.title
    if (choix == "2" ):
        getNext()
    if (choix == "3" ): 
        id_reddit = input ("Enter the ID of subreddit please ")
        trending_reddit = posts.loc[posts['id'] == id_reddit]



def getPosts():
    posting = []
    hot_posts = reddit.subreddit(str(trending_reddit.subreddit))
    # choosen_subreddit = reddit.subreddit(str(trending_reddit.subreddit))
    for post in hot_posts.hot(limit=10):
        posting.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posting = pd.DataFrame(posting,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    print(posting)       


def getComments():
    global trending_reddit,row
    tableComs = []
    comsRed = reddit.submission(id=trending_reddit.id)
    for reply in comsRed.comments : 
        if isinstance(reply, MoreComments):
            continue
        tableComs.append([reply.author,reply.body,reply.score])
    tableComs = pd.DataFrame(tableComs,columns=['Auteur','Commentaire','Score'])
    print(tableComs)
    for elm in tableComs.index : #Pour ecrire les commentaires dans un fichier excel
        worksheet.write(row,0,topic_trending)
        worksheet.write(row,1,str(tableComs['Auteur'][elm]))
        worksheet.write(row,2,str(tableComs['Commentaire'][elm]))
        worksheet.write(row,3,str(tableComs['Score'][elm]))
        row += 1



if __name__ == "__main__":
    getAll()
    getNext()
    current_id = 0
    print("You've choosen :"+str(trending_reddit.subreddit))
    workbook = xlsxwriter.Workbook(str(trending_reddit.subreddit)+'.xlsx') #Pour entrer dans le fichier excel et ècrire dedans nos données
    worksheet = workbook.add_worksheet() 
    worksheet.write(row,0,'Topic')
    worksheet.write(row,1,'Auteur')
    worksheet.write(row,2,'Commentaire')
    worksheet.write(row,3,'Score')
    input("Press any key to continue into Trending topics on your Subredit")
    getPosts()
    getNext()
    row += 1
    input ("Press any key to get comments ")
    getComments()
    workbook.close()