##Part 2
###Setting up database and migrations

In this section we're going to get our database set up to store the results of our word counts. Along the way we'll set up a Postgres database, set up SQLAlchemy to use as an ORM, and use Alembic for our data migrations.
<br>
Some things we'll use in this section:
<br>
Postgres - link <br>
SQLAlchemy - link <br>
Alembic - link <br>
Flask-Migrate - link <br>

To get started install Postgres on your local computer if you don't have it already. Since Heroku uses Postgres it will be good for us to develop locally on the same database. If you don't have Postgres installed Postgres.app is an easy way to get up and running quick for Mac users: http://postgresapp.com/. Once you have Postgres installed create a database called wordcount_dev to use as our local development database. In order to use our newly created database in our Flask app we're going to need to install a few things
```
$ pip install psycopg2, SQLAlchemy, Flask-Migrate
$ pip freeze > requirements.txt
```
Psycopg is is a python adapter for Postgres, SQLAlchemy is an awesome python ORM, Flask-Migrate will install both that extension and Alembic which we'll use for our database migrations. (note = if you're on Mavericks and having trouble installing psycopg2 check out http://stackoverflow.com/questions/22313407/clang-error-unknown-argument-mno-fused-madd-python-package-installation-fa)
<br>
Add the following line to the DevelopmentConfig class in your config.py file to set your app to use your newly created database in development.
```
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/wordcount_dev'
```
Now in your app.py file we're going to import SQLAlchemy and connect our database
```python
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run()
```

Now let's set up a basic model to hold the results of our wordcount. Add a new models.py file to your app
```
$ touch models.py
```
Within that file create a Result model
```python
from app import db

class Result(db.model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(db.JSON)
    result_no_stop_words = db.Column(db.JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id %r>' % self.id
```
What we are doing here is creating a table to store the results of our wordcount. We first import the database that we created in our app.py file. Next we create a Result class and assign it a table name of results. We then set the attributes that we want to store for a result - the id of the result we stored, the url that we counted the words of, a full list of words that we counted, and a list of words that we counted that doesn't include stop words (More on this later). We then create an __init__ method that will run the first time that we create a new result, and finally a __repr__ method to represent the object when we query for it.

We are going to use Alembic and Flask-Migrate to migrate our database to the latest version. We could 

Config for heroku databases
Deploy to heroku
Run heroku migrations

