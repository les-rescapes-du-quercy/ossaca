#! /usr/bin/python3
# -*- coding:utf-8 -*-
from flask import Flask, flash, render_template, request, g
from db_helpers import *
from upload import *

# ----------- GENERAL ----------- #

app = Flask(__name__)

app.secret_key = 'prouttrucmuche'

@app.route('/')

# ----------- DOGS ----------- #

@app.route('/dogs', methods=['GET', 'POST'])
def dogs():
    if request.method == 'POST':
        if 'id' in request.form:
            update_dog(request.form)
        else:
            id = add_new_dog(request.form)
            pictures = upload_image(request, id)
            update_pictures_dog(id, pictures)

    dlist = get_dogs()
    return render_template('dogs.html', dogs = dlist)

@app.route('/dogs/new_dog', methods=['GET'])
def new_dog():
    return render_template('new_dog.html')

@app.route('/dog', methods=['GET'])
def dog(species='dog', name=None):
    id = request.args.get('id', '')
    dog = getdb().get_dog_by_id(id)
    return render_template('animal.html', species=species, animal=dog)

# ----------- CATS ----------- #

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

# ----------- CARES ----------- #

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

# ----------- FOODS ----------- #

@app.route('/foods', methods=['GET', 'POST'])
def food():
    if request.method == 'POST':
        handle_bowl(request.form)
        handle_food(request.form)

    bowls = get_bowls()
    foods = get_foods()
    return render_template('admin-foods.html', bowls=bowls, foods=foods)

def handle_bowl(form):
    if 'id_add_bowl' in form:
        if form['id_add_bowl'] != "None":
            add_new_bowl(form);
    elif 'id_edit_bowl' in form:
        if form['id_edit_bowl'] != "None":
            update_bowl(form)
    elif 'id_del_bowl' in form:
        if form['id_del_bowl'] != "None":
            del_bowl(form['id_del_bowl'])

def handle_food(form):
    if 'id_add_food' in form:
        if form['id_add_food'] != "None":
            add_new_food(form);
    elif 'id_edit_food' in form:
        if form['id_edit_food'] != "None":
            update_food(form)
    elif 'id_del_food' in form:
        if form['id_del_food'] != "None":
            del_food(form['id_del_food'])

# ----------- BOXES ----------- #

@app.route('/boxes', methods=['GET', 'POST'])
def box():
    if request.method == 'POST':
        if 'id_del' in request.form:
            if request.form['id_del'] != "None":
                del_box(request.form['id_del'])
        elif 'id_edit' in request.form:
            if request.form['id_edit'] != "None":
                update_box(request.form)
        else:
            add_new_box(request.form);
    boxes = get_boxes()
    return render_template('admin-boxes.html', boxes=boxes)

# ----------- STATES ----------- #

@app.route('/states', methods=['GET', 'POST'])
def states():
    if request.method == 'POST':
        if 'id_del' in request.form:
            if request.form['id_del'] != "None":
                del_state(request.form['id_del'])
        elif 'id_edit' in request.form:
            if request.form['id_edit'] != "None":
                update_state(request.form)
        else:
            add_new_state(request.form);
    states = get_states()
    return render_template('admin-states.html', states=states)

# ----------- MAIN ----------- #

if __name__ == '__main__':
    app.run(debug=True)
