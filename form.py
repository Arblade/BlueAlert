import pandas as pd
import re
import time
import requests
import nltk
import heapq
from nltk.corpus import stopwords
import datetime
def get_pd(tweets):
    list_media=[]
    list_links=[]
    DetailsSet=pd.DataFrame()
    DataSet=pd.DataFrame()
    for tweet in tweets : 
        url=""
        type_media=""
        isvideo=False
        """
        # si vidéo
        if hasattr(tweet,'extended_entities' ) and 'media' in tweet.extended_entities.keys():
            for media in tweet.extended_entities['media']:
                if media['type']=="video":
                    isvideo=True
                    variants=media['video_info']['variants']
                    for variant in variants :
                        if variant['content_type']=="video/mp4":
                            url=variant['url']
                            type_media="video"
                            print("[-] >>>>>>>>>>>", type_media)
                            list_media+=[{"type":type_media, "url":url}]
                            break
                
        # sinon si image
        if (not isvideo) and  'media' in tweet.entities.keys():
            for media in tweet.entities['media']:
                url=media['media_url_https']
                type_media=media['type']
                print("[-] >>>>>>>>>>>", type_media)
                list_media+=[{"type":type_media, "url":url}]
    """
    DetailsSet['tweetID'] = [tweet.id for tweet in tweets]
    DataSet['tweetTime'] = [tweet.created_at for tweet in tweets]
    DataSet['authorVerified'] = [tweet.user.verified for tweet in tweets]
    for tweet in tweets : 
        if tweet.entities['urls']!=[]:
            for elem in tweet.entities['urls']:
                if elem['expanded_url'] not in list_links:
                    list_links.append(elem['expanded_url'])
        if "media" in tweet.entities.keys():
            for elem in tweet.entities['media']:
                if elem['media_url_https'] not in  list_media :
                    list_media.append({"type":elem['type'], "url" : elem['media_url_https']})
    print('[+] list liens',list_links)
    
    if len(DataSet['tweetTime'])!=0:
        now=datetime.datetime.now()-datetime.timedelta(hours=1)
        mmin=DataSet['tweetTime'][0]
        mmax=DataSet['tweetTime'][0]
        for k in range(len(DataSet['tweetTime'])):
            date=DataSet['tweetTime'][k]
            if date.to_pydatetime()>mmax:
                mmax=date
            if date.to_pydatetime()<mmin:
                mmin=date
            DataSet['tweetTime'][k]=str(now - DataSet['tweetTime'][k].to_pydatetime())[:-7]
        res=mmax-mmin
        hours=res.total_seconds()/3600.00
    else :
        print("[+] Aucun tweet")
        res="0"
    stats_time=res
    

        #ts.append(time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(date,'%a %b %d %H:%M:%S +0000 %Y')))

    l=[]
    for tweet in tweets :
        if hasattr(tweet, 'retweeted_status'):
            l.append(tweet.retweeted_status.full_text)
        else :
            l.append(tweet.full_text)
    
    #for i in range(len(l)) :
    #    res = res=re.sub(r'(http[^\s]*)',lambda x : requests.get(x.group()).url,l[i])
    #    l[i]=res
    DataSet['tweetText'] = l
    ensemble=[]
    for tweet in l :
        ensemble.append(tweet)
    #print("[+]", type( ensemble[0]))
    ensemble2=nltk.sent_tokenize(".".join(ensemble))
    #print("[+] nltk", ensemble2)
    for i in range (len(ensemble2)) :
        ensemble2[i]=ensemble2[i].lower()
        #print("\ntext non épuré")
        #print(ensemble2[i])
        ensemble2[i]=re.sub(r'\W', " ", ensemble2[i])
        
        ensemble2[i]=re.sub(r'\s+', " ", ensemble2[i])
        #print(ensemble2[i])
    wordfreq = {}
    all_stopwords = stopwords.words('english')+ stopwords.words('french')+["https","http","co"]
    for sentence in ensemble2:
        
        tokens = nltk.word_tokenize(sentence)

        tokens = [word for word in tokens if not word in all_stopwords]
        for token in tokens:
            if not token.isnumeric():
                if token not in wordfreq.keys():
                    wordfreq[token] = 1
                else:
                    wordfreq[token] += 1
    stats_words = heapq.nlargest(10, wordfreq, key=wordfreq.get)


    DetailsSet['tweetRetweetCt'] = [tweet.retweet_count for tweet in tweets]
    DetailsSet['tweetFavoriteCt'] = [tweet.favorite_count for tweet in tweets]
    # DataSet['tweetSource'] = [tweet.source for tweet in tweets]


    DetailsSet['userID'] = [tweet.user.id for tweet in tweets]
    DetailsSet['userScreen'] = [tweet.user.screen_name for tweet in tweets]
    DetailsSet['userName'] = [tweet.user.name for tweet in tweets]
    # DataSet['userCreateDt'] = [tweet.user.created_at for tweet 
    # in tweets]
    # DataSet['userDesc'] = [tweet.user.description for tweet in tweets]
    DataSet['userFollowerCt'] = [tweet.user.followers_count for tweet in tweets]
    # DataSet['userFriendsCt'] = [tweet.user.friends_count for tweet 
    # in tweets]
    # DataSet['userLocation'] = [tweet.user.location for tweet in tweets]
    # DataSet['userTimezone'] = [tweet.user.time_zone for tweet 
    # in tweets]
    return DataSet,DetailsSet,stats_time,stats_words,list_media,list_links

def get_info(res,details,num):
    print("\nInfo Tweet")
    print("Tweet published at {} by {}, {}".format(res['tweetTime'][num],details['userName'][num],details['userScreen'][num]))
    print("______________________________________________\n")
    print(res["tweetText"][num])
    print("https://twitter.com/{}/status/{}".format(details['userScreen'][num],details['tweetID'][num]))
    
    