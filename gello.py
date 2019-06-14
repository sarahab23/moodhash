import os
from flask import Flask,request,jsonify,render_template, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
import urllib.request
import subprocess

app=Flask(__name__)


y = []

@app.route("/",methods=['GET'])
def main():
	return render_template('index.html')

@app.route("/upload",methods=['GET','POST']
def upload():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		return 'file uploaded successfully!'
	else:
		return render_template('index.html')

"""
def image():
	cmd = "./darknet detector test cfg/combine9k.data cfg/yolo9000.cfg ../yolo9000-weights/yolo9000.weights data/abc.jpg -thresh 0.01"

	returned_value = subprocess.call(cmd, shell=True) 

	fo = open("file11.txt","r")
	li = fo.readlines()
	fo.close()

	for i in li[1:]:
		x = i.split(':')
		y.append(x[0])
	return jsonify(y)

"""

if __name__ == '__main__':
	app.run(debug=True)


