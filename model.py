from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///favourites.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:venuse123@database-1.clcrnnlay3xc.us-west-2.rds.amazonaws.com/vinkela'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('sqlite://', echo=False)
Base = declarative_base()

db = SQLAlchemy(app)
ma = Marshmallow(app)



# table for categories
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
# table for items
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    category_name = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('item', lazy=True))

    def __repr__(self):
        return '<Item %r>' % self.title

# table for logs
class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(80), nullable=True)
    date_modified = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        return '<Logs %r>' % self.title

# table for tags
class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(50), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'),
        nullable=False)
    category = db.relationship('Item',
        backref=db.backref('tags', lazy=True))


    def __repr__(self):
        return '<Tags %r>' % self.key

        
#for formatting object as json
class ItemSchema(ma.ModelSchema):
    class Meta:
        fields = ("id", "title","rank","category_name","description", "date_created")
        Model = Item 

class CategorySchema(ma.ModelSchema):
    class Meta:
        fields = ("id", "name", "date_created")
        Model = Category 

class LogsSchema(ma.ModelSchema):
    class Meta:
        fields = ("id", "title","category","description", "date_created", "action")
        Model = Logs 

class TagsSchema(ma.ModelSchema):
    class Meta:
        fields = ("id", "key","value","item_id")
        Model = Tags 

