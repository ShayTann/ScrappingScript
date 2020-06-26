blacklist = {"memes","porn","comedy"}
current = "comedyheaven"
statut = True
for word in blacklist :
    if current.find(word) != -1 :
        statut = False
if statut : 
    print("Nice")
else : 
    print("Go away")