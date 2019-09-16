Hi there! Thanks for veiwing my implementation!

My implementation makes uses of Flask framework for the APP and the API

The database is MySql with Sqlalchemy as the interface

The APP is hosted using AWS elastic Beanstalk and can be accessed via the url 

To test API, make sure all the dependencies in requirement.txt is installed in the environment. Then call python with
"python api.py"

The code for my implementation and other files as required can be found in www.https//github.com/orjikalu/favourites


The Model approach
The database "database-1" is hosted on AWS RDS
it consist of four tables/classes names
1. Items: For holding the items with the following fields id(primary key) category_id(which links it to Categories), title(unique key), description, tags, date_created, category_name(for easy indexing)

2. category: For holding items category with the following fields id(primary key), name, date_created. 
3. Logs: for holding all the activities on the database. it has the following fields title, category, date_modified,
3. Tags for holding item tags. it has an item_id field that links it to the item that owns it.

Reorder_priorities is contained in functions.py and as the name implies reorders the rank of all the items in a category when a new category is added.

app.py and api.py simply collects data from the user and either stores it in the database or collects data from the database and outputs to the user in the correct form.
app.py outputs to templates.
api.py outputs json.