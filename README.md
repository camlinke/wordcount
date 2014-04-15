Setting up a Staging and Production for Flask on Heroku

The app that’s being built is going to be a simple text box that you enter in a webpage and it processes and displays a count of how many times each word appears on the page (or twitter stream). In part one we'll set up a local development environment and then deploy both a staging environment and a production environment on Heroku. In part 2 we'll be doing a bunch of backend processing to count the words of a web page so we’ll implement a request queue that will do the actual processing of the words.

Setting up a basic "Hello World" app on Heroku with staging and production environments.

To get our initial setup created we're going to use Virtualenv and Virtualenvwrapper to help set things up. This will give us a few extra tools to help us silo our environment. I'm going to assume for this tutorial you've used a few things before:

Virtualenv - if not check this out.
Virtualenvwrapper - if not check this out.
Flask - If not check this tutorial out.
git/github - If not check out this tutorial.
Heroku (basic) - If not check out this tutorial.

Getting things set up:
First things first lets get a repo set up. Create a repo in Github (if you want) and clone it into your working directory. Alternatively init a new github repo. Next we're going to use Virtualenvwrapper to set up a new virtual environment by running the following command:

$ mkvirtualenv wordcount

This creates a new virtualenv for us. Along with creating a new virualenv it create some new options including Postactiveate. Postactive happens after you run the "workon" command to start your virtual environment. This is going to help us later when we are setting up some environement variables - but for now we're also going to use it to automatically jump is to our project when we first start it.

Open up the postactivate file - I find the easiest for this is to use vim by typing in the following command:

$ vi $VIRTUAL_ENV/bin/postactivate

Add the following line to your project:

cd ~/path/to/your/project

Now back on the command line type in:

$ workon wordcount

to restart your environment. You might not have noticed anything happen so open a new terminal windown and do it again, it will activate you environment and jump you to your project directory. This usually saves me a little bit of time, especially when I haven't worked on a project in a while and end up rummaging around trying to remember where I put it. In addition to this fun trick we're going to use postactivate set things like environment variables, keys, etc. later on.

Next we're going to get our basic structure for our app set up. Add the following files to your wordcount folder:

$ touch app.py .gitignore README.md requirements.txt

This will give you the following structure (note, the readme and gitignore files should have been created already if you cloned a github project that you set up.):

Wordcount
    app.py
    .gitignore
    README.md
    requirements.txt

Next we'll install flask:

$ pip install flask

and add the installed libraries to our requirements.txt file

$ pip freeze > requirements.txt

Open up app.py in your favorite editor and add the following code:

from flask import Flask
app = Flask(__name__)

```python
@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
```

Run the app and you should see

































