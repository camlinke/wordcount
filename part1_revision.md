# Flask by Example - Part 1: Project Setup

Welcome! Today we're going to build an app with a simple text box that you enter in a webpage and it processes and displays a count of how many times each word appears on the page (or twitter stream). In part one, we'll set up a local development environment and then deploy both a staging environment and a production environment on Heroku. In part two, we'll be doing a bunch of backend processing to count the words of a web page so we’ll implement a request queue that will do the actual processing of the words.

## Setup

We'll start with a *basic "Hello World" app on Heroku with staging and production environments*.

To get our initial setup created we're going to use Virtualenv and Virtualenvwrapper. This will give us a few extra tools to help us silo our environment. I'm going to assume for this tutorial you've used the following tools before: 

- Virtualenv - [http://www.virtualenv.org/en/latest/](http://www.virtualenv.org/en/latest/)
- Virtualenvwrapper - [http://virtualenvwrapper.readthedocs.org/en/latest/](http://virtualenvwrapper.readthedocs.org/en/latest/)
- Flask - [http://flask.pocoo.org/](http://flask.pocoo.org/)
- git/Github - [http://try.github.io/levels/1/challenges/1](http://try.github.io/levels/1/challenges/1)
- Heroku (basics) - [https://devcenter.heroku.com/articles/getting-started-with-python](https://devcenter.heroku.com/articles/getting-started-with-python) 

First things first, let's get a repo set up. Create a repo in Github (if you want) and clone it into your working directory. Alternatively initialize a new git repo within your working directory:

```
$ git init
```

Next, we're going to use Virtualenvwrapper to set up a new virtual environment by running the following command:

```
$ mkvirtualenv wordcount
```

This creates a new virtualenv for us. Along with creating a new virtualenv, it creates some new options including *Postactivate* - which happens after you run the `workon` command to start your virtual environment. This is going to help us later when we are setting up some environment variables - but for now we're also going to use it to automatically jump to our project when we first start it.

Open up the *postactivate* file. The easiest way to do this is with VIM: 

```
$ vi $VIRTUAL_ENV/bin/postactivate
```

Add the following line to your project:

```
cd ~/path/to/your/project
```

*Make sure to alter the above command for your environment. For example, my working directory is on my desktop - so my path is: `cd ~/desktop/wordcount`.*

> Within VIM, press "i" to enter the INSERT mode. Paste the above line in the file, then press  "escape" to exit INSERT mode. Finally press ":", then "w", and finally "q" to save and exit VIM. 

Now open a new terminal window and run the following command:

```
$ workon wordcount
```

If all is setup properly, it will activate your environment and move you directly to the project directory. A nice timesaver. :)

Next we're going to get our basic structure for our app set up. Add the following files to your wordcount folder:

```
$ touch app.py .gitignore README.md requirements.txt
```

This will give you the following structure:

```
Wordcount
├── README.md
├── app.py
└── requirements.txt
```

The *.gitignore* file should have been created already if you cloned the project. If not, you can grab the contents from the [repo](https://github.com/camlinke/wordcount).

Next install Flask:

```
$ pip install flask
```

Add the installed libraries to our *requirements.txt* file:

```
$ pip freeze > requirements.txt
```

Open up app.py in your favorite editor and add the following code to *app.py*:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
```

Run the app:

```
$ python app.py
```

And you should see your basic Hello world app in action on [http://localhost:5000/](http://localhost:5000/).

Next we're going to set up our Heroku environments for both our production and staging app.

## Setup Heroku

I'm going to assume you have the Heroku toolchain installed. For more basic information about setting up your Heroku app for use with Python see the earlier link.

After you have Heroku setup on your machine create a Procfile:

```
$ touch Procfile
```

Add the following line to your newly created file

```python
web: gunicorn app:app
```

Make sure to add gunicorn to your requirments.txt file

```
$ pip install gunicorn
$ pip freeze > requirements.txt
```

Commit your changes in git and optionally PUSH to Github, then create two new Heroku apps.

One for production:

```
$ heroku create wordcount-pro
```

And one for staging (or pre-production):

```
$ heroku create wordcount-stage
```

Add your new apps to your git remotes. Make sure to name one pro (for "production") and the other stage (for "staging"):

```
$ git remote add pro git@heroku.com:YOUR_APP_NAME.git
$ git remote add stage git@heroku.com:YOUR_APP_NAME.git
```

Now we can push both of our apps live to Heroku.

For staging:
```
$ git push stage master
```

For production:

```
$ git push pro master
```

Once both of those have been pushed, navigate to them and see that your app is working on both URLs. 

Let's make a change to our app and push only to staging:

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

Test it out by adding a name after the URL. For example: [http://localhost:5000/mike](http://localhost:5000/mike).

Now we want to try out our changes on staging before we push them live to production. Make sure your changes are committed in git and push your work up to staging:

```
$ git push stage master
```

Now if you navigate to your staging environment, you'll be able to use the new `/<name>` url and get "Hello <name>" based on what you put into the URL as the output. However, if you try the same thing on the production site you will get an error. *So we can build things and test them out on staging and then when we're happy, push them live to production.* 

Let's push our site to production now that we're happy with it:

```
$ git push pro master
```

Now we have the same functionality live on our production site. 

*This staging/production workflow allows us to make changes, show things to clients, within a sandboxed serve without causing any changes to the live production site that users are using.*

## Config Settings

The last thing that we're going to do is set up different config environments for our app. Often there are things that are going to be different between your local, staging, and production setups. You’ll want to connect to different databases, have different AWS keys, etc. Let’s set up a config file to deal with the different servers. Add a config.py file to your project

```
$ touch config.py
```

With our config file we're going to borrow a bit from how Django's config is set up. We'll have a base config class that the other config classes inherit from. Then we'll import the appropriate config class as needed. 

Add the following to your newly created *config.py* file:

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

We set up a base Config class with some basic setup that our other config classes inherit from. Now we will be able to import the appropriate config class based on the situation that we're in.

So, now we can use environment variables to choose which settings we’re going to use based on the environment (e.g., local, staging, production). 

### Local Settings

To set up our `APP_SETTINGS` variable locally, we are going to use our Virtualenvwrapper *postactivate* file again.

Add the following line to your *postactivate* file: 

```
export APP_SETTINGS="config.DevelopmentConfig"
```

Reload your environment by running the workon wordcount command again:
```
$ workon wordcount
```

Now when you run your app it will import from the configuration that you set up in your `DevelopmentConfig` class.

### Heroku Settings

Similarly we’re going to set environment variables on Heroku. 

For staging run the following command:

```
$ heroku config:set APP_SETTINGS=config.StagingConfig --remote stage
```

For production:

```
$ heroku config:set APP_SETTINGS=config.ProductionConfig --remote pro
```

To make sure we use the right environment change *app.py*:

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

We imported `os` and we used the `os.environ` method to import the appropriate `APP_SETTINGS` variables, depending on our environment. We then set up the config in our app with the `app.config.from_object` method.

Commit and push your changes to both staging and production (and Github if you have it setup). 

Want to test the environment variables out to make sure it's detecting the right environment? Add a print statement to *app.py*: 

```python
print os.environ['APP_SETTINGS']
```

Now when you run the app, it will show which config settings it's importing:

**Local**:

```
$ python app.py
config.DevelopmentConfig
```

**Staging**:

```
$ heroku run python app.py --app wordcount-pro
Running `python app.py` attached to terminal... up, run.2830
config.ProductionConfig
```

**Production**:

```
$ heroku run python app.py --app wordcount-stage
Running `python app.py` attached to terminal... up, run.1360
config.StagingConfig
```


<hr>

With the setup out of the way, we're going to start to build out the word counting functionality of this app in the next part. Along the way, we'll add a request queue to set up background processing for the word count portion, as well dig further into our Heroku setup by adding setting up the configuration and migrations for our database which we'll use to store our wordcount results.

Best!
