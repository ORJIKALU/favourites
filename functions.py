import requests
from flask import redirect, render_template, request, session
from model import app, db, Item, Category, Logs
from operator import itemgetter, attrgetter


# reassigns priorities when an item is added
def reorder_priorities(Category):
    items = Item.query.filter_by(category_id=int(Category))
    if items == None:
        return None
    sort = False
    previous = False

    sorted_items = sorted(items, key = attrgetter("rank"))
        
    for item in sorted_items:
        if sort:
            item.rank = item.rank + 1
        else:
            if previous != False:
                if item.rank == previous.rank:
                    previous.rank = previous.rank + 1
                    sort = True
        previous = item
    db.session.commit()
