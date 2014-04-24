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

from models import Result

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
from sqlalchemy.dialects.postgresql import JSON

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id %r>' % self.id
```
What we are doing here is creating a table to store the results of our wordcount. We first import the database that we created in our app.py file as well as JSON from sqlalchemy's postgresql dialects. Next we create a Result class and assign it a table name of results. We then set the attributes that we want to store for a result - the id of the result we stored, the url that we counted the words of, a full list of words that we counted, and a list of words that we counted that doesn't include stop words (More on this later). We then create an __init__ method that will run the first time that we create a new result, and finally a __repr__ method to represent the object when we query for it.
<br>
We are going to use Alembic and Flask-Migrate to migrate our database to the latest version. Alembic is migration library for SQLAlchemy and could be used without Flask-Migrate if you want. However Flask-Migrate does help with some of the setup and makes things easier. You installed Alembic and Flask-Migrate earlier when you ran pip install Flask-Migrate. 
<br>
Create a new file called manage.py
```
$ touch manage.py
```
In order to use Flask-Migrate we need to import Manager as well as Migrate and MigrateCommand to our manage.py file. We also import app and db so we have access to them within our manage script. We first set our config to get our environment based on our environment variabile and then we create a migrate instance with app and db as the arguments and set up a manager command to initialize a Manager instance for our app. Finally we add the 'db' command to our manager so that we can run our migrations from the command line.

```python
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from app import app, db
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
```
In order to run our migrations we first must initialize alembic
```
$ python manage.py db init
  Creating directory /Users/camlinke/Dropbox/realpython/wordcount/migrations ... done
  Creating directory /Users/camlinke/Dropbox/realpython/wordcount/migrations/versions ... done
  Generating /Users/camlinke/Dropbox/realpython/wordcount/migrations/alembic.ini ... done
  Generating /Users/camlinke/Dropbox/realpython/wordcount/migrations/env.py ... done
  Generating /Users/camlinke/Dropbox/realpython/wordcount/migrations/env.pyc ... done
  Generating /Users/camlinke/Dropbox/realpython/wordcount/migrations/README ... done
  Generating /Users/camlinke/Dropbox/realpython/wordcount/migrations/script.py.mako ... done
  Please edit configuration/connection/logging settings in '/Users/camlinke/Dropbox/realpython/wordcount/migrations/alembic.ini' before proceeding.
```
After you run the database initialization you will see a new folder called migrations is in your project. This holds the setup necessary for alembic to run migrations on your project. Inside of it you will see that it has a folder called versions that will contain the migration scripts as they are created. Let's create our first migration by running the migrate command.
```
$ python manage.py db migrate
  INFO  [alembic.migration] Context impl PostgresqlImpl.
  INFO  [alembic.migration] Will assume transactional DDL.
  INFO  [alembic.autogenerate.compare] Detected added table 'results'
  Generating /Users/camlinke/Dropbox/realpython/wordcount/migrations/versions/20ff8063fe45_.py ... done
```
Now you'll notice in your versions folder there is a migration file. This file is autogenerated by Alembic based on the model that you have create. You could generate this file yourself, however for a lot of cases the autogenerated file will do.
<br>
Now we'll apply our upgrades to our database using the db upgrade command:
```
$ python manage.py db upgrade
  INFO  [alembic.migration] Context impl PostgresqlImpl.
  INFO  [alembic.migration] Will assume transactional DDL.
  INFO  [alembic.migration] Running upgrade None -> 20ff8063fe45, empty message
```
Our database is now ready for us to use in our app. Finally we are going to apply these migrations to our Heroku databases.

Shows up in the migrations file
Create our first migration
Run our first migration

Config for heroku databases
Deploy to heroku
Run heroku migrations

