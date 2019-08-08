import os
from flask import Flask,request,jsonify,render_template, redirect, url_for,flash,session,abort,jsonify
from werkzeug.utils import secure_filename
from flask import send_from_directory
import urllib.request
import subprocess
import nltk 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
import re
import nltk
from gensim.models import Word2Vec
import requests 
import cv2
import pytesseract


UPLOAD_FOLDER = '/home/arpan/moodhash1/darknet/data'
ALLOWED_EXTENSIONS = set(['jpg'])

app=Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def algorithm(wd):    

	#print('in  function')
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
	model=Word2Vec(allcaptions,size=300,window=20,min_count=9)
	words=model.wv.vocab

	similar=model.wv.most_similar(wd)

	ans=''

	for i in similar:
		ans=ans+'#'+i[0]+' '

	return ans





@app.route("/")
def upload():
    return render_template('index.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
       
     
       # imgfile = request.files['file']
       # img = cv2.imread(imgfile.filename,0)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #print(img)
       # st = pytesseract.image_to_string(img)
       # print(imgfile.filename)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      

            cmd = "./darknet detector test cfg/combine9k.data cfg/yolo9000.cfg ../yolo9000-weights/yolo9000.weights data/"+filename+" -thresh 0.01 > file11.txt"

            returned_value = subprocess.call(cmd, shell=True) 
    return redirect("file:///Users/sanju/Desktop/moodhash/frontend/index.html#about",code=300,Response=None)
            
@app.route('/returnanswer', methods=['GET'])
def jaimatadi():
            fo = open("file11.txt","r")
            li = fo.readlines()
            fo.close()
            cmd="rm file11.txt"
            y=[]
            for i in li[1:]:
                    x = i.split(':')
                    y.append(x[0])


           # img = cv2.imread('predictions.png')
            #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #st = pytesseract.image_to_string(img)
            
                 # print(y)
            hashtag=''
            final=''
            #lu = st.split(' ')
           # for i in lu:
           #         final=final+'#'+i+' '
            for i in y:
                    hashtag=hashtag+i+' '
                    final=final+'#'+i+' '
            hashtag=hashtag.lower()
            hashtag=re.sub(r'\s+',' ',hashtag)   
            hashtag=re.sub(r'\s+'," ",hashtag) 
            tags=hashtag.split(' ')
	    #print(tags)
            
            for i in tags :
                    try:
                            #print('calling func')
                            ans=algorithm(i)
                           # print('in looop')
                            #print(ans)
                            final=final+ans+' '
                    except:
                            #print('in except')192.168.21.0
                            continue

            print(final)
            return final
	
            
            returned_value = subprocess.call(cmd, shell=True)




@app.route("/caption",methods=['GET', 'POST'])

def caption():
        if request.method == 'POST':
                caption = request.form['caption']
                stop_words = set(stopwords.words('english')) 
	  
                lst=[',',';',':','@','!','$','%','&','-','_','?','.','*']
	#txt=input()
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
                #print(xx)
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
                                #print('calling func')
                                ans=algorithm(i)
                                #print('in looop')
                                #print(ans)
                                final=final+ans+' '
                        except:
                                #print('in except')
                                continue
   
                return render_template('index.html', xx = final)
        else:
             return render_template('index.html')    

"""
@app.route("/tags1",methods=['GET', 'POST'])
def tags():
        if request.method == 'POST':
                tags = request.form['tags']
                lt = tags.split(" ")
                return render_template('index.html',lt = lt)
        else:
             return render_template('index.html')    
"""


@app.route('/tags', methods=['POST'])
def index():
    
	if request.method == 'POST':
		hashtag =request.form['tags']
		#print(hashtag)
		#hashtag=request.json['name']

		hashtag=hashtag.lower()
		hashtag=re.sub(r'\s+',' ',hashtag)   
		hashtag=re.sub(r'\s+'," ",hashtag) 
		tags=hashtag.split(' ')
		#print(tags)
		final=''
		for i in tags :
			try:
				#print('calling func')
				ans=algorithm(i)
				#print('in looop')				
				#print(ans)
				final=final+ans+' '
			except:
				#print('in except')
				continue
		#print(final)    
		return render_template('index.html',final = final)

@app.route('/pro',methods=['POST'])
def funct():
    
    try:
        handle=request.forms['handle']
        link=propic(handle)
        return render_template('index.html',link=link)
    except:
        
        link='https://instagram.fblr2-1.fna.fbcdn.net/vp/c39ffd126353a1558f215e8373c208a6/5D8363C3/t51.2885-19/s320x320/24332224_155214565207012_1366344017297539072_n.jpg?_nc_ht=instagram.fblr2-1.fna.fbcdn.net'
        return jsonify({'link':link})

if __name__ == '__main__':
        app.run(debug=True)
