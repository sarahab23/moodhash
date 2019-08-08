import requests
from flask import Flask,request,jsonify,redirect
import re
import nltk
from gensim.models import Word2Vec

app = Flask(_name_)
app.config['DEBUG'] = True


import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize,sent_tokenize
import requests
import re
from gensim.models import Word2Vec
import os
 


def algorithm(wd):    


    link='https://www.instagram.com/explore/tags/{}/?__a=1'
    url=link.format(wd)

    r = requests.get(url).json()
    num1=len(r['graphql']['hashtag']['edge_hashtag_to_media']['edges'])
    num2=len(r['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges'])

    recentposts=r['graphql']['hashtag']['edge_hashtag_to_media']['edges']
    topposts=r['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges']

    #print(num1)
    #print(num2)


    allcaptions=[]
    text=''

    for i in range(0,num1):
        try:
            x=recentposts[i]['node']['edge_media_to_caption']['edges'][0]['node']['text']
            m = re.findall(r'[#]\w+',x)
            t=''

            for j in m:
                t=t+j+' '
            t=re.sub(r'\#',' ',t)
            t=t.lower()
            #text=text+t+' '
            allcaptions.append(nltk.word_tokenize(t))

        except:
            continue
    for i in range(0,num2):
        try:
            x=topposts[i]['node']['edge_media_to_caption']['edges'][0]['node']['text']
            m = re.findall(r'[#]\w+',x)
            t=''

            for j in m:
                t=t+j+' '
            t=re.sub(r'\#',' ',t)
            t=t.lower()
            #text=text+t+' '
            for k in range(0,1):
                allcaptions.append(nltk.word_tokenize(t))

        except:
            continue






        #print(allcaptions)
    m = re.findall(r'[t]\w+',text)    
    text=nltk.word_tokenize(text)    
    model=Word2Vec(allcaptions,size=300,window=30,min_count=10)
    words=model.wv.vocab

    similar=model.wv.most_similar(wd)
    
    ans=''
    
    for i in similar:
        ans=ans+'#'+i[0]+' '
    
    return ans


def propic(instaid):
    idlink='https://www.instagram.com/{}/?__a=1'
    url=idlink.format(instaid)

    data=requests.get(url).json()

    user=data['graphql']['user']['profile_pic_url_hd']

    return user



def comcap(instaid):
    idlink='https://www.instagram.com/{}/?__a=1'
    url=idlink.format(instaid)

    data=requests.get(url).json()
    if(data['graphql']['user']['is_private']):
    
        return 'oops its a private account'
    user=data['graphql']['user']['edge_owner_to_timeline_media']['edges']
    
    num=len(user)
    #print(num)
    
    allcap=''
    
    for i in range(0,num):
        try:
            x=user[i]['node']['edge_media_to_caption']['edges'][0]['node']['text']
            m = re.findall(r'[#]\w+',x)
            t=''

            for j in m:
                t=t+j+' '
            t=re.sub(r'\#',' ',t)
            t=t.lower()
            allcap=allcap+t+' '
        except:
            continue
       
    
    from collections import Counter
    data_set = allcap
    # split() returns list of all the words in the string
    split_it = data_set.split()
    
    # Pass the split_it list to instance of Counter class.
    Counter = Counter(split_it)
    #print(Counter)

    # most_common() produces k frequently encountered
    # input values and their respective counts.
    most_occur = Counter.most_common(8)
    txt=''
    for i in most_occur:
        txt=txt+'#'+i[0]+' '
    #print(txt)


    return txt



@app.route('/<string:text>', methods=['GET'])
def index(text):
    
    if request.method == 'GET':
        hashtag = text
        #hashtag=request.json['name']
        
        hashtag=hashtag.lower()
        hashtag=re.sub(r'\s+',' ',hashtag)   
        hashtag=re.sub(r'\s+'," ",hashtag) 
        tags=hashtag.split(' ')
        final=''
        moodhash=''
        for i in tags :
            try:
                ans=algorithm(i)
                final=final+ans+' '
            except:
                continue    
        for i in final :
            moodhash='#'+i+' '
        
        return jsonify({'answer':final})

@app.route('/pro/<string:handle>',methods=['GET'])
def funct(handle):
    
    try:

        link=propic(handle)
        
    except:
        
        link='https://instagram.fblr2-1.fna.fbcdn.net/vp/c39ffd126353a1558f215e8373c208a6/5D8363C3/t51.2885-19/s320x320/24332224_155214565207012_1366344017297539072_n.jpg?_nc_ht=instagram.fblr2-1.fna.fbcdn.net'
        


    try:
        ans=comcap(handle)
        

    except:

        ans="The id isn't public or it doesn't exist " 
   #elif request.method == 'GET':
    #    return render_template('hash.html')


    return jsonify({'link':link,'ans':ans})

'''   
@app.route('/upload',methods=['POST'])
def image():
    try:
        print("in uploads")
        
        photo = request.files['photo']
        print(photo.filename)
    except:
        print('in except')    


    return redirect('file:///Users/sanju/Desktop/moodhash/frontend/index.html#about',code=302,Response=None) '''   



@app.route("/caption/<string:capti>",methods=['GET'])

def caption(capti):
        if request.method == 'GET':
                caption = capti
                stop_words = set(stopwords.words('english')) 
	  
                lst=[',',';',':','@','!','$','%','&','-','_','?','.','*']
	
                txt = caption
	  
	  
                tokenized = sent_tokenize(txt) 
                for i in tokenized: 
	      
                        wordsList = nltk.word_tokenize(i) 

                        wordsList = [w for w in wordsList if not w in stop_words and not w in lst]  

                        tagged = nltk.pos_tag(wordsList) 

                lst1=['NN','NNS','NNP','NNPS','VBG']
                xx=[]

                for i in range(len(tagged)):
                        if tagged[i][1] in lst1:
                               xx.append(tagged[i][0])
              
               # return jsonify(y)
                print(xx)
                final=''
                hashtag=''
                for i in xx:
                        hashtag=hashtag+i+" "
                for i in xx:
                        final=final+'#'+i+' '
                hashtag=hashtag.lower()
                hashtag=re.sub(r'\s+',' ',hashtag)   
                hashtag=re.sub(r'\s+'," ",hashtag) 
                tags=hashtag.split(' ')
	        #print(tags)
            
                for i in tags :
                        try:
                                print('calling func')
                                ans=algorithm(i)
                                print('in looop')
                                print(ans)
                                final=final+ans+' '
                        except:
                                print('in except')
                                continue
   
                return jsonify({'cap':final})
