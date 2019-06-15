import os
from flask import Flask,request,jsonify,render_template, redirect, url_for,flash,session,abort,jsonify
from werkzeug.utils import secure_filename
from flask import send_from_directory
import urllib.request
import subprocess


UPLOAD_FOLDER = '/home/sarah/Desktop'
ALLOWED_EXTENSIONS = set(['jpg'])

app=Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

y = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def upload():
    return render_template('index.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        """file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'file uploaded successfully'
        
        caption = request.form['caption']
        """
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file uploaded successfuly'
    else:
        return render_template('index.html')
"""

def image():
	cmd = "./darknet detector test cfg/combine9k.data cfg/yolo9000.cfg ../yolo9000-weights/yolo9000.weights data/person.jpg -thresh 0.01 > file11.txt"

	returned_value = subprocess.call(cmd, shell=True) 

	fo = open("file11.txt","r")
	li = fo.readlines()
	fo.close()

	for i in li[1:]:
		x = i.split(':')
		y.append(x[0])
	return jsonify(y)
	
	cmd="rm file11.txt"
	returned_value = subprocess.call(cmd, shell=True)
	
"""
if __name__ == '__main__':
	app.run(debug=True)
