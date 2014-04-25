##Part 2
###Setting up database and migrations

In this section we're going to get our database set up to store the results of our word counts. Along the way we'll set up a Postgres database, set up SQLAlchemy to use as an ORM, and use Alembic for our data migrations.
<br>
Some things we'll use in this section:
<br>
Postgres - [http://www.postgresql.org/](http://www.postgresql.org/) <br>
SQLAlchemy - [http://www.sqlalchemy.org/](http://www.sqlalchemy.org/) <br>
Alembic - [http://alembic.readthedocs.org/en/latest/](http://alembic.readthedocs.org/en/latest/) <br>
Flask-Migrate - [http://flask-migrate.readthedocs.org/en/latest/](http://flask-migrate.readthedocs.org/en/latest/) <br>

To get started install Postgres on your local computer if you don't have it already. Since Heroku uses Postgres it will be good for us to develop locally on the same database. If you don't have Postgres installed Postgres.app is an easy way to get up and running quick for Mac users: http://postgresapp.com/. Once you have Postgres installed create a database called wordcount_dev to use as our local development database. In order to use our newly created database in our Flask app we're going to need to install a few things
```
$ pip install psycopg2, SQLAlchemy, Flask-Migrate
$ pip freeze > requirements.txt
```
Psycopg is is a python adapter for Postgres, SQLAlchemy is an awesome python ORM, Flask-Migrate will install both that extension and Alembic which we'll use for our database migrations. (if you're on Mavericks and having trouble installing psycopg2 check out this link [http://stackoverflow.com/questions/22313407/clang-error-unknown-argument-mno-fused-madd-python-package-installation-fa](http://stackoverflow.com/questions/22313407/clang-error-unknown-argument-mno-fused-madd-python-package-installation-fa))
<br>
Add the following line to the DevelopmentConfig class in your config.py file to set your app to use your newly created database in development.
```
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
```
Similar to how we added an environment variable in the last post we are going to add a DATABASE_URL variable to our postactivate file. Using VIM you can do this in the following way: <br>
Open your file in VIM
```
$ vi $VIRTUAL_ENV/bin/postactivate
```
Hit 'i' on your keyboard to insert text. Add the following line to your file:
```
export DATABASE_URL="postgresql://localhost/wordcount_dev"
```
Now hit escape and type 'wq' and then enter to save and close vim. Restart your environment:
```
$ workon wordcount
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
  Creating directory /wordcount/migrations ... done
  Creating directory /wordcount/migrations/versions ... done
  Generating /wordcount/migrations/alembic.ini ... done
  Generating /wordcount/migrations/env.py ... done
  Generating /wordcount/migrations/env.pyc ... done
  Generating /wordcount/migrations/README ... done
  Generating /wordcount/migrations/script.py.mako ... done
  Please edit configuration/connection/logging settings in '/wordcount/migrations/alembic.ini' before proceeding.
```
After you run the database initialization you will see a new folder called migrations is in your project. This holds the setup necessary for alembic to run migrations on your project. Inside of it you will see that it has a folder called versions that will contain the migration scripts as they are created. Let's create our first migration by running the migrate command.
```
$ python manage.py db migrate
  INFO  [alembic.migration] Context impl PostgresqlImpl.
  INFO  [alembic.migration] Will assume transactional DDL.
  INFO  [alembic.autogenerate.compare] Detected added table 'results'
  Generating /wordcount/migrations/versions/20ff8063fe45_.py ... done
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
<br>
First we need to add the details or our staging and production databases to our config file. To check if you have a database set up on your staging server run
```
$ heroku config --app stage-wordcount3000
```
You should see something similar to the following - specifically the DATABASE_URL part.
```
$ heroku config --app stage-wordcount3000
  === stage-wordcount3000 Config Vars
  APP_SETTINGS:               config.StagingConfig
  DATABASE_URL:               postgres://info:about/my/database
  HEROKU_POSTGRESQL_NAVY_URL: postgres://info:about/my/database
```
If only the APP_SETTINGS part is there we need to add the Postgres addon to your stage servers. Run the following to add the Postgres addon to your heroku app:

```
$ heroku addons:add heroku-postgresql:dev --app stage-wordcount3000
  Adding heroku-postgresql:dev on stage-wordcount3000... done, v11 (free)
  Attached as HEROKU_POSTGRESQL_NAVY_URL
  Database has been created and is available
  ! This database is empty. If upgrading, you can transfer
  ! data from another database with pgbackups:restore.
  Use `heroku addons:docs heroku-postgresql` to view documentation.
```
Now when we run heroku config again we should the connection settings for our URL. Similar to how we set up the config for our local database, we are going to import the uri of our database in from the environment variable. Add the following line to both the staging and production config classes that you have set up in config.py
```python 
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
```
Your config.py file should now look like this
```python
import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class StagingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class TestingConfig(Config):
    TESTING = True
```
Now when our config gets loaded into our app the appropriate database will be connected to it as well.
Next we need to commit the changes that you've made to git and push your staging server
```
$ git push stage master
```
Finally we need to run the migrations that we have created to migrate our staging database. We do this by using the heroku run command to run python scripts within our heroku app. We will use this to run the same db upgrade command from our manage.py file.
```
$ heroku run python manage.py db upgrade --app stage-wordcount3000
  Running `python manage.py db upgrade` attached to terminal... up, run.4755
  INFO  [alembic.migration] Context impl PostgresqlImpl.
  INFO  [alembic.migration] Will assume transactional DDL.
  INFO  [alembic.migration] Running upgrade None -> 20ff8063fe45, empty message
```
Note how we only ran the upgrade, not the init or migrate commands. We already have our migration setup and ready to go, we only need to run it on our heroku database.
<br>
Let's now do the same for our production site. Set up a database for your production app. Push your changes to your production site. Notice how you don't have to make any changes to your config file, it's setting the database based on the newly created DATABASE_URL environment variable. Finally run your migrations on your production server.
```
$ heroku addons:add heroku-postgresql:dev --app wordcount3000
$ git push pro master
$ heroku run python manage.py db upgrade --app wordcount3000
```
Now both our our stage and production sites have their databases set up and are migrated and ready to go. In Part 3 we're going to build the word counting functionality and have it sent to a request queue to deal with the long running wordcount.

Best!