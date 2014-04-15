Setting up a Staging and Production for Flask on Heroku

The app that’s being built is going to be a simple text box that you enter in a webpage and it processes and displays a count of how many times each word appears on the page (or twitter stream). In part one we'll set up a local development environment and then deploy both a staging environment and a production environment on Heroku. In part 2 we'll be doing a bunch of backend processing to count the words of a web page so we’ll implement a request queue that will do the actual processing of the words.

Setting up a basic "Hello World" app on Heroku with staging and production environments.

To get our initial setup created we're going to use Virtualenv and Virtualenvwrapper to help set things up. This will give us a few extra tools to help us silo our environment. I'm going to assume for this tutorial you've used a few things before, I've included links to where you can find our more information about each if you havn't.

Virtualenv - if not check this out.
Virtualenvwrapper - if not check this out.
Flask - If not check this tutorial out.
git/github - If not check out this tutorial.
Heroku (basic) - If not check out this tutorial.


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
See http://www.realpython.com/blog/python/migrating-your-django-project-to-heroku/ for more basic information about setting up your heroku app for use iwth Python. There is some Django specific stuff in there, however most of it applies to any python setup.

After you have Heroku setup on your machine create a Procfile
```
$ touch Procfile
```
and add the line
```python
web: gunicorn app:app
```
to your newly created file. Make sure to add gunicorn to your requirments.txt file
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
Once both of those have been pushed you can navigate to them and see that your app is working on both URLs. 































