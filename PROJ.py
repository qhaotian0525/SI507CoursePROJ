# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 21:31:37 2022

@author: 18639
"""

import json
import requests
import praw
import webbrowser
import os.path
import matplotlib.pyplot as plt
import re

#IMDb
api_key="k_dtekjptm"

#Reddit
c_id='oBYF1kSa0HNBZdwXgx--DA'
c_secret='eTjI8K91-KrF58v7cMU6PqUDpCC2wg'
u_agent='si507proj'




class movie:
    def __init__(self,j):
        self.title=j['title']
        self.poster=j['image']
        if j['imDbRating']!=None:
            
            self.rating=float(j['imDbRating'])
        else:
            self.rating=None
        self.imbdid=j['id']
        self.plot=j['plot']
        self.rtime=j['runtimeStr']
        self.genre=j['genres']
        self.stars=j['stars']
        self.des=j['description']
        self.wikiurl=None
        self.youtube=None
        if j['genreList']!=None and len(j['genreList'])!=0:
            self.genrekey=list([x["key"] for x in  j['genreList']])
        else:
            self.genreky=[]
        self.genrelist=j['genreList']
        self.starlist=j['starList']
        if j['starList']!=None and len(j['starList'])>0:
            self.director=j['starList'][0]['name']
        else:
            self.director=None
    def brief_info(self):
        if self.director!=None:
            return self.title+self.des+" by Director "+self.director
        else:
            return self.title+self.des
    def info(self):
        print("Title: ",self.title+self.des)
        print("Movie Runtime: ",self.rtime)
        print("Genre: ",self.genre)
        print("IMDb Rating: ",self.rating)
        print("Directed and acted by: ",self.stars)
        print("Plot Introduction: ",self.plot)
    def get_Wiki(self):
        url='https://imdb-api.com/en/API/Wikipedia/'+api_key+"/"+self.imbdid
        a=requests.get(url)
        wiki=json.loads(a.text)
        wikiurl=wiki['url']
        if wikiurl!=None:
            if len(wikiurl)>=5:
                self.wikiurl=wikiurl
                webbrowser.open(wikiurl)
            else:
                print("No WikiPedia Available")
                
        else:
            print("No WikiPedia Available")
    
    def get_poster(self):
        img=self.poster
        if img!=None:
            if len(img)>=5:
                webbrowser.open(img)
            else:
                print("No Poster Available")
        else:
            print("No Poster Available")
    
    def get_youtube(self):
        url='https://imdb-api.com/en/API/YouTubeTrailer/'+api_key+"/"+self.imbdid
        a=requests.get(url)
        ytb=json.loads(a.text)
        ytburl=ytb['videoUrl']
        if ytburl!=None :
            if len(ytburl) >5:
                print(ytburl)
                self.youtube=ytburl
                webbrowser.open(ytburl)
            else:
                print("Youtube Not Available")
                
        else:
            print("Youtube Not Available")
    
    def gen_dict(self):
        j={}
        j['title']=self.title
        j['image']=self.poster
        j['imDbRating']=self.rating
        j['id']=self.imbdid
        j['plot']=self.plot
        j['runtimeStr']=self.rtime
        j['genres']=self.genre
        j['stars']=self.stars
        j['description']=self.des
        j['Wiki']=self.wikiurl
        j["Youtube"]=self.youtube
        j['genreList']=self.genrelist
        j['starList']=self.starlist
        return j
    
class Reddit:
    def __init__(self,j,cache=False):
        if cache==False:
            
            self.title=j.title
            self.url="https://www.reddit.com/"+j.permalink
            self.num=j.num_comments
        else:
            self.title=j['title']
            self.url= j['url']
            self.num=j['num_comments']
    def info(self):
        return self.title+" [Number of Comments: "+str(self.num)+' ]'
    def look(self):
        webbrowser.open(self.url)
    def gen_dict(self):
        j={}
        j['title']= self.title
        j['url']=self.url
        j['num_comments']=self.num
        return j
        
        
url_imdb="https://imdb-api.com/API/AdvancedSearch/"+api_key+"?"

def imdb_search(searchterm,keyword):
    if searchterm=="title":
        url=url_imdb+"title="+keyword
    elif searchterm=="genres":
        url=url_imdb+"genres="+keyword
    obj=requests.get(url)
    obj=json.loads(obj.text)
    res=obj['results']
    count=0
    if len(res)==0:
        print('empty!')
        return
    else:
        movielist=[movie(j) for j in res]
        for m in movielist:
            count+=1
            print(str(count)+" "+m.brief_info())
        return movielist
    
    
    
def get_input(num=False):
    if num==False:
        t=input("Do you have specific titles? [y/n] ")
        while True:
            if t=="y":
                searchterm="title"
                kw=input("Please input the title: ")
                kw=kw.lower()
                return searchterm,kw
            elif t=="n":
                searchterm="genres"
                kw=input("Please input the genre: ")
                kw=kw.lower()
                return searchterm,kw
            elif t=="quit":
                return -1,-1
            else:
                t=input("Invalid input. Please type \"y\" or \"n\" " )
        
    else:
        n=input("Please select the number or type (\"r\") to return to search: ")
        if n=="quit":
            return -1
        elif n=="r":
            return n
        elif n.isnumeric():
            
            return n
        else:
            print("Invalid input!")
            return get_input(True)
        
        
def get_reddit(kw):
    reddit = praw.Reddit(client_id=c_id, client_secret=c_secret, user_agent=u_agent) #redirect_uri="http://localhost:8080",
    res=reddit.subreddit("movies").search(kw,limit=20)
    redlist=[]
    for i in res:
        redlist.append(Reddit(i))
    return redlist

###############################################################
def command_tree(tree):
    que,lft,rgt=tree
    stop=1
    if lft!=None and rgt!=None:
        while stop==1:
            t=input(que)
            if t=='y':
                stop=0
                return command_tree(rgt)
            
            elif t=='n':
                stop=0
                return command_tree(lft)
            elif t=='quit':
                return -1
            else:
                stop=1
                print("Invalid input")
    else:
        return que()
def get_genres():
    searchterm='genres'
    kw=input("Please input the genre: ")
    kw=kw.lower()
    return imdb_search(searchterm,kw) 

def get_titles():
    searchterm='title'
    kw=input("Please input the title: ")
    kw=kw.lower()
    return imdb_search(searchterm,kw) 

def get_cache():
    st="title"
    global cache_imdb
    kw=input("Please input the title: ")
    kw=kw.lower()
    print("Searching in Cache...")
    ttlist=[x['title'].lower() for x in cache_imdb]
    res_may=[]
    ctt=0
    for i in range(len(ttlist)):
        if re.search(kw.lower(),ttlist[i])!=None:
            ctt+=1
            entr=movie(cache_imdb[i])
            print(str(ctt)+" "+entr.brief_info())
            res_may.append(entr)
    if len(res_may)==0:
        print("Empty in Local Cache")
        movielist=imdb_search(st,kw)
    else:
        movielist=res_may
    return movielist

tree=("Do you have specific titles? [y/n]: ",(get_genres,None,None),("Do you want the local cache? [y/n]: ",(get_titles,None,None),(get_cache,None,None)))

          
######################################################      
if os.path.isfile("cache.txt"):
    with open("cache.txt") as f:
        c=f.read()
        buffer=json.loads(c)
    cache_imdb=buffer["cache_imdb"]
    cache_red=buffer['cache_red']
    len_imdb=buffer['len_imdb']
    len_red=buffer['len_red']
    genre_dict=buffer['genre_dict']
    rating_dict=buffer['rating_dict']

else:
    buffer={}
    cache_imdb=[]
    cache_red=[]
    len_imdb=[]
    len_red=[]
    genre_dict={}
    rating_dict={}
    for i in range(10):
        s=str(i)+" to "+str(i+1)
        rating_dict[s]=0
    
def main():
    ''' if os.path.isfile("cache.txt"):
        with open("cache.txt") as f:
            c=f.read()
            buffer=json.loads(c)
        cache_imdb=buffer["cache_imdb"]
        cache_red=buffer['cache_red']
        len_imdb=buffer['len_imdb']
        len_red=buffer['len_red']
        genre_dict=buffer['genre_dict']
        rating_dict=buffer['rating_dict']

    else:
        buffer={}
        cache_imdb=[]
        cache_red=[]
        len_imdb=[]
        len_red=[]
        genre_dict={}
        rating_dict={}
        for i in range(10):
            s=str(i)+" to "+str(i+1)
            rating_dict[s]=0'''

    stopp=0
    stoppp=0
    total_count=0
    total_count_red=0
    print("Welcome to Movie Searching System!")
    while True:
        if stopp==1:
            break
        ''' st,kw=get_input()
        if st==-1:
           
            break
        if st=="title":
            permit=input("Do you want the local cache? [y/n]: ")
            if permit=='y':
                
                print("Searching in Cache...")
                ttlist=[x['title'].lower() for x in cache_imdb]
                res_may=[]
                ctt=0
                for i in range(len(ttlist)):
                    if re.search(kw.lower(),ttlist[i])!=None:
                        ctt+=1
                        entr=movie(cache_imdb[i])
                        print(str(ctt)+" "+entr.brief_info())
                        res_may.append(entr)
                if len(res_may)==0:
                    print("Empty in Local Cache")
                    movielist=imdb_search(st,kw)
                else:
                    movielist=res_may
            else:
                movielist=imdb_search(st,kw)
        elif st=="genres":
            movielist=imdb_search(st,kw)'''
        movielist=command_tree(tree)
        if movielist==-1:
            break
        
      
        while True:
            if stoppp==1:
                
                stopp=1
                break
            num=get_input(num=True)
            if num==-1:
                
                stopp=1
                break
            elif num=="r":
                break
            elif int(num)<=len(movielist) and int(num)>=1:
                total_count+=1
                idx=int(num)-1
                entr=movielist[idx]
                d=entr.gen_dict()
                if d not in cache_imdb:
                    cache_imdb.append(entr.gen_dict())
                if entr.rating!=None:
                    r_range=str(int(entr.rating))+" to "+str(int(entr.rating+1))
                    
                    try:
                        rating_dict[r_range]+=1
                    except:
                        rating_dict[r_range]=0
                for gg in entr.genrekey:
                    try :
                        genre_dict[gg]+=1
                    except:
                        genre_dict[gg]=1
                    
                entr.info()
                while True:
                    i=input("Poster[p] / Wiki[w] / Youtube[y] / Reddit[red] /Return[r] /Quit[quit]:")
                    if i=="p":
                        entr.get_poster()
                        continue
                    elif i=="w":
                        entr.get_Wiki()
                        continue
                    elif i=="y":
                        entr.get_youtube()
                        continue
                    elif i=="red":
                        p_red=input("Do you want the local cache of Reddit? [y/n]: ")
                        if p_red=="y":
                            print("Searching in cache...")
                            rr=[]
                            redtt=[x['title'].lower() for x in cache_red]
                            for i in range(len(redtt)):
                                if re.search(entr.title.lower(),redtt[i]) !=None:
                                    rr.append(Reddit(cache_red[i],cache=True))
                            if len(rr)==0:
                                print("No result in cache!")
                                redlist=get_reddit(entr.title)
                            else:
                                redlist=rr
                        else:
                            
                            
                            redlist=get_reddit(entr.title)
                        if len(redlist)==0:
                            print("No Content on Reddit")
                            continue
                        else:
                            count=0
                            for c in redlist:
                                count+=1
                                print(str(count)+" "+c.info())
                            while True:
                                nn=input("Please input the number or Return [r]: ")
                                if nn.isnumeric():
                                    if int(nn)<=len(redlist) and int(nn)>=1:
                                        total_count_red+=1
                                        idx=int(nn)-1
                                        en=redlist[idx]
                                        en.look()
                                        enc=en.gen_dict()
                                        if enc not in cache_red:
                                            
                                            cache_red.append(enc)
                                    else:
                                        print("Invalid Input")
                                elif nn=="r":
                                    break
                                else:
                                    print("Invalid Input")                                         
                    elif i=="r":
                        break
                    elif i=='quit':
                        stoppp=1
                        break
                    else:
                        print("Invalid Input!")
                            
                                            
                                    
                else:
                    print("Out of Range!")
    try:
        l_imdb=len_imdb[-1]
    except:
        l_imdb=0
    try:
        l_red=len_red[-1]
    except:
        l_red=0
    len_imdb.append(total_count+l_imdb)
    len_red.append(total_count_red+l_red)
    buffer["cache_imdb"]=cache_imdb
    buffer['cache_red']=cache_red
    buffer['len_imdb']=len_imdb
    buffer['len_red']=len_red
    buffer['genre_dict']=genre_dict
    buffer['rating_dict']=rating_dict
    buffer_str=json.dumps(buffer)
    with open("cache.txt",'w') as f:
        f.write(buffer_str)
    yy=0
    while True:
        if yy!='y':
            
            yy=input("View the statistics of your searching history? [y/n]: ")
        if yy=="n":
            print("Bye!")
            break
        elif yy=="y":
            
            print("What data do you want?")
            print("[a] Searching Times from IMDb this time")
            print("[b] Searching Times from IMDb all history")
            print("[c] Searching Times from Reddit this time")
            print("[d] Searching Times from Reddit all history")
            print("[e] Genres statistics all history long")
            print("[f] Ratings statistics all history long")
            choice=input("Please type [a]/[b]/.../[f]/[quit]: ")
            if choice=='a':
                try:
                    l=len_imdb[-1]-len_imdb[-2]
                except:
                    l=len_imdb[0]
                print("You have searched for "+str(l)+" times from IMDb this time.")
            elif choice=='b':
                g=input("Graph [g] or Text [t]: ")
                if g=='g':
                
                    plt.figure("F1")
                    plt.plot(len_imdb,'.-')
                    plt.xlabel("Searching Order")
                    plt.ylabel("Total Searching Times (IMDb)")
                    plt.show()
                elif g=="t":
                    str1="Your searching history from IMDb is: { "
                    for i in len_imdb:
                        str1=str1+str(i)+" "
                    str1+="}"
                    print(str1)
            
            elif choice=='c':
                try:
                    l=len_red[-1]-len_red[-2]
                except:
                    l=len_red[0]
                print("You have searched for "+str(l)+" times from Reddit this time.")
                
            elif choice=='d':
                g=input("Graph [g] or Text [t]: ")
                if g=='g':
                    plt.figure("F2")
                    plt.plot(len_red,'.-')
                    plt.xlabel("Searching Order")
                    plt.ylabel("Total Searching Times (Reddit)")
                    plt.show()
                elif g=="t":
                    str1="Your searching history from Reddit is: { "
                    for i in len_red:
                        str1=str1+str(i)+" "
                    str1+="}"
                    print(str1)
            elif choice=='e':
                g=input("Graph [g] or Text [t]: ")
                if g=='g':
                    plt.figure("F3")
                    plt.bar(genre_dict.keys(),genre_dict.values())
                    plt.show()
                elif g=="t":
                    str1="Your genre statistics is: "
                    print(str1)
                    for i in genre_dict.keys():
                        print(i+" : "+str(genre_dict[i]))
            elif choice=="quit":
                idx=list(genre_dict.values()).index(max(list(genre_dict.values())))
                print("Your Most Frequent Searching Genre Now is: ",list(genre_dict.keys())[idx])
                print("Bye!")
                break
            
            elif choice=='f':
                plt.figure("F4")
                plt.xlabel("Rating Distribution")
                plt.ylabel("Numbers")
                plt.bar(rating_dict.keys(),rating_dict.values())
                plt.show()
            else:
                print("Invalid")
                        
                        
                    
    
if __name__ =="__main__":
    main()
                    
        
        
        
            
            
            
            
        
    
        
        
