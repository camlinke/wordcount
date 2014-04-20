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
Now let's set up a basic model to hold the results of 