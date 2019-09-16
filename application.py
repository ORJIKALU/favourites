import os
from flask import Flask, flash, redirect, render_template, request, session
from model import app, db, Item, Category, Logs, Tags
from functions import reorder_priorities 
from tempfile import mkdtemp
import datetime
from operator import itemgetter, attrgetter
from sqlalchemy import and_
from flask import jsonify




# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
    
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "precious_two"
app.config["SECURITY_PASSWORD_SALT"] = "precious"

error = None

@app.route("/")
def home_page():
    """login page"""
    categories = Category.query.all()
    items = Item.query.all()
    items = sorted(items, key = attrgetter("rank"))
    logs = Logs.query.all()
    return render_template("add_new_fav.html",items=items, categories=categories, logs=logs)

#add new item to items
@app.route("/add_new_fav", methods=["POST"])
def add_new_fav():
    category_id = int(request.form.get("choose_category"))
    item = request.form.get("title").lower()
    if not item:
        flash("Item must have a name", category="error")
        return redirect("/")
    if not category_id:
        flash("please select a category", category="error")
        return redirect("/")
    if not request.form.get("ranking"):
        flash("Please select a rank for item", category="error")
        return redirect("/")
    if request.form.get("description"):
        if len(request.form.get("description")) < 10:
            flash('please describe the item in more details')
            return redirect("/")
    titles = Item.query.filter_by(title=item)
    current_category = Category.query.filter_by(id=category_id).first()
    for title in titles:
        if category_id == int(current_category.id) and title.title == item:
            flash(title.title+" already exist in "+current_category.name, category="error")
            return redirect("/")
    category_row = Category.query.filter_by(id=int(request.form.get("choose_category"))).first()
    item = Item(title = request.form.get("title").lower(), description = request.form.get("description"), category_name =category_row.name,category_id=category_row.id, rank=request.form.get("ranking"))
    db.session.add(item)
    db.session.commit()
    reorder_priorities(int(request.form.get("choose_category")))
    titles = Item.query.filter_by(title=request.form.get("title").lower()).first()
    if request.form.get("no_of_tags"):
        n = int(request.form.get("no_of_tags"))
        for i in range(n):
            j = i + 1
            key_name = "key"+str(j)
            value_name = "value"+str(j)
            if request.form.get(key_name) and request.form.get(value_name):
                tag = Tags(key = request.form.get(key_name), value=request.form.get(value_name), item_id=titles.id)
                db.session.add(tag)
    log = Logs(title=item.title,category=item.category_name, action="added")
    db.session.add(log)
    db.session.commit()
    flash(request.form.get("title")+" added to "+current_category.name, category="message")

    return redirect("/")
    
# add new category to categories
@app.route("/add_category", methods=["POST"])
def add_category():
    if request.form.get("category"):
        new_category = request.form.get("category").upper()
        current = Category.query.filter_by(name=new_category).first()
        if current:
            flash(new_category+" already exist in categories", category=error)
            return redirect("/")
        category = Category(name=new_category)
        db.session.add(category)
        db.session.commit()
        log = Logs(action="added", category=category.name)
        db.session.add(log)
        db.session.commit()
        flash(request.form.get("category").upper()+" added to Categories", category="message")
        return redirect("/")
    else:
        flash("category must have a name", category="error")
        return redirect("/")


    

#check if item exist in categories already using ajax
@app.route("/item_check", methods=["POST"])
def item_check():
    category_id = int(request.form.get("category"))
    item = request.form.get("title").lower()
    titles = Item.query.filter_by(title=item)
    current_category = Category.query.filter_by(id=category_id).first()
    for title in titles:
        if category_id == int(current_category.id) and title.title == item:
            return jsonify(title=item,response='fail', category=current_category.name)
        else:
            return jsonify(title=item,response='pass', category=current_category.name)
    return jsonify(title=item,response='pass', category=current_category.name)
    

#check if categories already exist in Categories using ajax
@app.route("/category_check", methods=["POST"])
def category_check():
    new_category = request.form.get("category").upper()
    current = Category.query.filter_by(name=new_category).first()
    if current:
        return jsonify(response='fail', category=current.name)
    else:
        return jsonify(response='pass', category=new_category)
