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
        if 'id' in request.form:
            update_dog(request.form)
        else:
            add_new_dog(request.form)

    dlist = get_dogs()
    return render_template('dogs.html', dogs = dlist)

@app.route('/dogs/new_dog', methods=['GET', 'POST'])
def new_dog():
        return render_template('new_dog.html')

@app.route('/dog', methods=['GET'])
def dog(species='dog', name=None):
    id = request.args.get('id', '')
    dog = getdb().get_dog_by_id(id)
    return render_template('animal.html', species=species, animal=dog)

@app.route('/cats', methods=['GET', 'POST'])
def cats():
    if request.method == 'POST':
        if 'id' in request.form:
            update_cat(request.form)
        else:
            add_new_cat(request.form)

    clist = get_cats()
    return render_template('cats.html', cats = clist)

@app.route('/cats/new_cat', methods=['GET', 'POST'])
def new_cat():
    return render_template('new_cat.html')

@app.route('/cat', methods=['GET'])
def cat(species='cat', name=None):
    id = request.args.get('id', '')
    cat = getdb().get_cat_by_id(id)
    return render_template('animal.html', species=species, animal=cat)

@app.route('/cares', methods=['GET', 'POST'])
def cares(cares=None):
    if request.method == 'POST':
        if 'id_del' in request.form:
            if request.form['id_del'] != "None":
                del_care(request.form['id_del'])
        elif 'id_edit' in request.form:
            if request.form['id_edit'] != "None":
                update_care(request.form)
        else:
            add_new_care(request.form);
    cares = get_cares()
    return render_template('admin-cares.html', cares=cares)

if __name__ == '__main__':
    app.run(debug=True)
