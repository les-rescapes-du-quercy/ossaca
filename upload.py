#! /usr/bin/python3
# -*- coding:utf-8 -*-
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = 'uploads/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(request, type, upload_dir):
    if type not in request.files:
        return redirect(request.url)
    file = request.files[type]
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_dir, filename))

def upload_image(request, id):
    if request.method == 'POST':
        dog_name = request.form['name'].replace(" ", "_")
        dog_dir = str(id) + "_" + dog_name.lower()
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], "images", dog_dir)
        os.mkdir(upload_dir)
        upload_file(request, "img", upload_dir)
