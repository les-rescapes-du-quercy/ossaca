#! /usr/bin/python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, g
from flask_images import Images, ImageSize, resized_img_src
from db_helpers import *

app = Flask(__name__)

app.config['IMAGES_PATH'] = ['images']
app.config['IMAGES_NAME'] = 'images'

app.secret_key = 'prouttrucmuche'
images = Images(app)

@app.route('/')
@app.route('/dogs', methods=['GET', 'POST'])
def dogs():
    if request.method == 'POST':
        add_new_dog(request.form)
    dlist = get_dogs()
    return render_template('dogs.html', dogs = dlist)

@app.route('/dogs/new_dog.html', methods=['GET', 'POST'])
def new_dog():
        return render_template('new_dog.html')

@app.route('/cats')
def cats():
    return render_template('cats.html')

@app.route('/admin-care')
def admin():
    return render_template('admin-care.html')

@app.route('/dog', methods=['GET'])
def dog(name=None):
    id = request.args.get('id', '')
    name = getdb().get_dog_by_id(id).name
    return render_template('dog.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
