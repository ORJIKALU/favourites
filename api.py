from flask import Flask,session
from model import app, db, Item, Category, Logs, Tags, ItemSchema, CategorySchema, LogsSchema, TagsSchema
from functions import reorder_priorities 
import datetime
from operator import itemgetter, attrgetter
from sqlalchemy import and_
from flask import jsonify
from flask import Flask, flash, redirect, render_template, request, session


from flask_restful import reqparse, abort, Api, Resource
from flask_restful import fields, marshal_with


api = Api(app)

#query database
categories = Category.query.all()
items = Item.query.all()
items = sorted(items, key = attrgetter("rank"))
logs = Logs.query.all()
tags = Tags.query.all()



#shows all items with their categories
class Items(Resource):
    def get(self):
        Item_Schema = ItemSchema(many=True)
        output = Item_Schema.dump(items)  
        return jsonify({'Items':output})

# Category
# shows a all Category and lets you add a category
class Categories(Resource):
    def get(self):
        Category_Schema = CategorySchema(many=True)
        output = Category_Schema.dump(categories)  
        return jsonify({'Categories':output})

    def post(self):
        if request.args.get("category"):
            new_category = request.form.get("category").upper()
            current = Category.query.filter_by(name=new_category).first()
            if current:
                abort(404, message="{} already exist".format(new_category))
            category = Category(name=new_category)
            db.session.add(category)
            db.session.commit()
            log = Logs(action="added", category=category.name)
            db.session.add(log)
            db.session.commit()
            return jsonify({'Success':"{} added successfully".format(new_category)})
        else:
            abort(404, message="please enter name for category")


#all the logs 
class Logs(Resource):
    def get(self):
        Log_Schema = LogsSchema(many=True)
        output = Log_Schema.dump(logs)  
        return jsonify({'Logs':output})

#all the logs 
class Single_item(Resource):
    def get(self, title):
        item_row = Item.query.filter_by(title=title.lower()).first()
        if  item_row == None:
                abort(404, message="Item {} doesn't exist".format(title))

        Item_Schema = ItemSchema()
        output = Item_Schema.dump(item_row)  
        return jsonify({'Item':output})
    
    def post(self):
        category_name = request.args.get("category_name").upper()
        item = request.args.get("title").lower()
        if not item:
            abort(404, message="please enter name for item")
        if not category_name:
            abort(404, message="please enter category for item")
        if not request.form.get("ranking"):
            abort(404, message="please a rank for item")
        if request.form.get("description"):
            if len(request.form.get("description")) < 10:
                abort(404, message="please provide more description for item")
        titles = Item.query.filter_by(title=item)
        current_category = Category.query.filter_by(id=category_name).first()
        for title in titles:
            if category_name == current_category.name and title.title == item:
                abort(404, message="{} already exist in {}".format(item, category_name))
        category_row = Category.query.filter_by(name=category_name).first()
        item = Item(title = request.args.get("title").lower(), description = request.args.get("description"), category_name =category_row.name,category_id=category_row.id, rank=request.args.get("ranking"))
        db.session.add(item)
        db.session.commit()
        reorder_priorities(int(category_row.id))
        log = Logs(title=item.title,category=item.category_name, action="added")
        db.session.add(log)
        db.session.commit()
        return jsonify({'Success':"{} added successfully to {}".format(item.title, item.category_name)})


# all the items categories and logs
class All(Resource):
    def get(self):
        Item_Schema = ItemSchema(many=True)
        Category_Schema = CategorySchema(many=True)
        Log_Schema = LogsSchema(many=True)
        Tag_Schema = TagsSchema(many=True)
        output1 = Category_Schema.dump(items)  
        output2 = Category_Schema.dump(categories)  
        output3 = Log_Schema.dump(logs)  
        output4 = Tag_Schema.dump(tags)  

        return jsonify({'Items':output1},{'Categories':output2},{'Logs':output3},{'Tags':output4})


# all the categories with the items they contain
class Items_given_category(Resource):
    def get(self, category_name):
        category_row = Category.query.filter_by(name=category_name.upper()).first()
        if  category_row == None:
                abort(404, message="Todo {} doesn't exist".format(category_name))
        cat_array=[]
        for item in items:
            if item.category_id == category_row.id:
                cat_array.append(
                    {"title":item.title, "description":item.description,"rank":item.rank, "date_created":item.date_created}
                )
        return jsonify({category_name.upper():cat_array})
        
        Item_Schema = ItemSchema(many=True)
        output = Item_Schema.dump(items)  
        return jsonify({'Items':output})




#api endpoints
api.add_resource(All, '/')
api.add_resource(Items, '/items')
api.add_resource(Single_item, '/items/<title>')
api.add_resource(Logs, '/logs')
api.add_resource(Categories, '/categories')
api.add_resource(Items_given_category, '/categories/<category_name>')


if __name__ == '__main__':
    app.run(debug=True)

