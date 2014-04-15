Setting up a Staging and Production for Flask on Heroku

The app that’s being built is going to be a simple text box that you enter in a webpage and it processes and displays a count of how many times each word appears on the page (or twitter stream). In part one we'll set up a local development environment and then deploy both a staging environment and a production environment on Heroku. In part 2 we'll be doing a bunch of backend processing to count the words of a web page so we’ll implement a request queue that will do the actual processing of the words.

Setting up a basic "Hello World" app on Heroku with staging and production environments.

To get our initial setup created we're going to use Virtualenv and Virtualenvwrapper to help set things up. This will give us a few extra tools to help us silo our environment. I'm going to assume for this tutorial you've used a few things before, I've included links to where you can find our more information about each if you havn't.

Virtualenv - http://www.virtualenv.org/en/latest/ <br>
Virtualenvwrapper - http://virtualenvwrapper.readthedocs.org/en/latest/ <br>
Flask - http://flask.pocoo.org/ <br>
git/github - http://try.github.io/levels/1/challenges/1 <br>
Heroku (basic) - http://www.realpython.com/blog/python/migrating-your-django-project-to-heroku/ <br>


Getting things set up:
First things first lets get a repo set up. Create a repo in Github (if you want) and clone it into your working directory. Alternatively init a new github repo. Next we're going to use Virtualenvwrapper to set up a new virtual environment by running the following command:
```
$ mkvirtualenv wordcount
```
This creates a new virtualenv for us. Along with creating a new virualenv it create some new options including Postactiveate. Postactive happens after you run the "workon" command to start your virtual environment. This is going to help us later when we are setting up some environement variables - but for now we're also going to use it to automatically jump is to our project when we first start it.

Open up the postactivate file - I find the easiest for this is to use vim by typing in the following command:
```
$ vi $VIRTUAL_ENV/bin/postactivate
```
Add the following line to your project:
```
cd ~/path/to/your/project
```
Now back on the command line type in:
```
$ workon wordcount
```
to restart your environment. You might not have noticed anything happen so open a new terminal windown and do it again, it will activate you environment and jump you to your project directory. This usually saves me a little bit of time, especially when I haven't worked on a project in a while and end up rummaging around trying to remember where I put it. In addition to this fun trick we're going to use postactivate set things like environment variables, keys, etc. later on.

Next we're going to get our basic structure for our app set up. Add the following files to your wordcount folder:
```
$ touch app.py .gitignore README.md requirements.txt
```
This will give you the following structure (note, the readme and gitignore files should have been created already if you cloned a github project that you set up.):

```
Wordcount
    app.py
    .gitignore
    README.md
    requirements.txt
```

Next we'll install flask:

```
$ pip install flask
```

and add the installed libraries to our requirements.txt file

```
$ pip freeze > requirements.txt
```

Open up app.py in your favorite editor and add the following code:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
```

Run the app
```
$ python app.py
```
and you should see your basic Hello world app in action.

Next we're going to set up our Heroku environments for both our production and staging app.

Setup Heroku
I'm going to assume you have the heroku toolchain installed. For more basic information about setting up your heroku app for use with Python see the earlier link - There is some Django specific stuff in there, however most of it applies to any python setup.

After you have Heroku setup on your machine create a Procfile
```
$ touch Procfile
```
and add the following line to your newly created file
```python
web: gunicorn app:app
```
Make sure to add gunicorn to your requirments.txt file
```
$ pip install gunicorn
$ pip freeze > requirements.txt
```
Commit your changes in git and head to Heroku to create two new apps. You can do this from the command line if you choose, I find it really easy to set up in the Heroku dashboard however. Click create new app and create the production version for your app. I've named my app wordcount3000. Head back to your command line and add the following line, where YOUR_APP is the name of your app.
```
remote add production git@heroku.com:YOUR_APP.git
```
in my case this is:
```
remote add production git@heroku.com:wordcount3000.git
```

In a simliar manner we're going to follow the same process to create a staging server. Create a new Heroku app and name it stage-YOUr_APP, in my case this is stage-wordcount3000. Back on the command line set up that repo with stage instead of production:
```
$ git remote add stage git@heroku.com:stage-YOUR_APP.git
```
for me this is:
```
$ git remote add stage git@heroku.com:stage-wordcount3000.git
```
Now we can push both of our apps live to Heroku.
For stage:
```
$ git push stage master
```
For production
```
$ git push production master
```
Once both of those have been pushed you can navigate to them and see that your app is working on both URLs. Let's make a change to our app and push only to stage. Change your app to:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run()
```

Run your app locally to make sure everything is working
```
$ python app.py
```
Now we want to try out our changes on stage before we push them live to production. Make sure your changes are comitted in git and push your work up to stage
```
$ git push stage master
```

Now if you navigate to your stage environment you'll be able to use the new /<name> url and get "Hello <name>" based on what you put into the URL. However if you try the same thing on the production site you will get an error. So we can build things and test them out on stage and then when we're happy push them live. Let's push our site to production now that we're happy with it
```
$ git push production master
```
Now we have our funcationality live on our production site. This stage/production system allows us to make changes, show things to clients, use a sandboxed payment server, etc. without causing any changes to the live production site that users are using.

The last thing that we're going to do is set up our different config environments for our app as well as stage and production databases. Often there are things that are going to be different between your local, stage, and production setups. You’ll want to connect to different databases, have different AWS keys, etc. Let’s set up a config file to deal with the different servers. Add a config.py file to your project
```
$ touch config.py
```
With our config file we're going to borrow a bit from how Django's config is set up. We'll have a base config class that the other config classes can inherit from. Then we'll import the appropriate config class as needed. Add the following to your newly created config.py file:
```python
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
```
We set up a base Config class with some basic setup that our other config classes inherit from. Now we will be able to import the appopriate config class based on the situation that we're in.
<br>
<br>
Now we’re going to use environment variables to choose which settings we’re going to use. We import os and add add a line to use the config based on an environment variable called "APP_SETTINGS"
<br>
Locally: <br>
To set up our APP_SETTINGS variable locally we are going to use our Virtualenvwrapper postactivate file again to set the APP_SETTINGS variable. <br>
Add the following line to your postactivate file 
```
export APP_SETTINGS="config.DevelopmentConfig"
```
Reload your environment by running the workon wordcount command again.
```
$ workon wordcount
```
Now when you run your app it will import from the configuration that you set up in your DevelopmentConfig class.
<br>
On Heroku: <br>
Similarly we’re going to set environment variables on Heroku. For staging run the following comand:
```
$ heroku config:set APP_SETTINGS=config.StagingConfig --remote stage
```

For production:
```
$ heroku config:set APP_SETTINGS=config.StagingConfig --remote production
```
To make sure we use the right environment change your app.py file to be:
```python
from flask import Flask
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run()
```
We imported os and we use the os.environ method to get the APP_SETTINGS variables that we set up in both staging and production. we then set up the config in our app with the app.config.from_object method. <br>
Commit and push your changes to both stage and production. Now we will be pulling each config settings for each environment that we are in.



























