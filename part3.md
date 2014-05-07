##Part 3
###Counting Words in a Request Queue

In this section we're going to count words from a webpage that the user enters, send the counting off to a request queue, and finally store the results in the migrated databases that we created last time.
<br>
To get started let's get rid of the hello world part that we've added to our app.py file and set up our index route to have a form to accept our url to count. Let's start by adding a templates folder to hold our templates and add an index.html file to it.
```
$ mkdir templates
$ touch index.html
```
Set up a very basic html page in the index.html file
```html
<html>
    <head>
        <title>Wordcount</title>
    </head>
    <style type="text/css">
        .content {
            width: 960px;
            height: 100%;
            margin-left: auto;
            margin-right: auto;
            margin-top: 100px;
            text-align: center;
        }
        #url-box {
            width: 300px;
            height: 30px;
            font-size: 19px;
        }
        button {
            height: 29px;
            font-size: 19px;
        }
    </style>
    <body>
        <div class="content">
            <h1>Wordcount3000</h1>
            <form method='POST' action='/'>
                <input type="text" name="url" placeholder="Enter URL..." id="url-box">
                <button type="submit" value="Submit">Submit</button>
            </form>
        </div>
    </body>
</html>
```
Now we need to have our index route serve that page. Change your app.py file to
```python
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Result

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
```
We are importing render_template from flask so that we can use our newly created template. We are then changing our index route to serve that file. Note we also changed our route to be:
'''python
@app.route('/', methods=['GET', 'POST'])
'''
The reason is that we are going to use that same route for both our GET request when we serve the index.html page, and the POST request when the user submits the url form.
<br>
Next we create a basic index.html file to set up our homepage:
```html
<html>
    <head>
        <title>Wordcount</title>
    </head>
    <style type="text/css">
        .content {
            width: 960px;
            height: 100%;
            margin-left: auto;
            margin-right: auto;
            margin-top: 100px;
            text-align: center;
        }
        #url-box {
            width: 300px;
            height: 30px;
            font-size: 19px;
        }
        #results {
            width: 100%;
            height: 100%;
        }
        table {
            margin: 0 auto;
        }
        thead {
            text-align: left;
        }
        button {
            height: 29px;
            font-size: 19px;
        }
        h3 {
            color: red;
        }
    </style>
    <body>
        <div class="content">
            <h1>Wordcount3000</h1>
            {% for error in errors %}
                <h3>{{ error }}</h3>    
            {% endfor %}
            <form method='POST' action='/'>
                <input type="text" name="url" placeholder="Enter URL..." id="url-box">
                <button type="submit" value="Submit">Submit</button>
            </form>
        </div>
    </body>
</html>
```
We have a bit of styling to make the page not completely hideous. Then we create a form with a textbox for people to be able to enter their url. Additionally we use a jinja for loop to loop through any errors and display them above our form.
<br>
Now we are going to use the requests library (which is awesome) to get the URLs submitted by the form. 
```
$ pip install requests
$ pip freeze > requirements.txt
```
Change your index route to the following:
```python
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import os
import requests

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Result

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        #get url that the person has entered
        try:
            url = request.form['url']
            if 'http://' not in url[:7]:
                url = 'http://' + url
            r = requests.get(url)
            print r.text
        except:
            errors.append("Unable to get URL, please make sure it's valid and try again")
    return render_template('index.html', errors=errors, results=results)
```
The first thing we do here is import the requests library and from flask we import request. Next we add a couple of variable to capture our errors so we can display them to the user, and set up our results as an empty dictionary initially. Next we add an if statement to check if the method of the request is a POST (note: don't confuse request, which comes from flask, and requests, which is the library we imported). If the user is posting the form we get the value of the textfield, which we have named 'url', from the form and assign it to a url variable. We do a little clean up on the entry to see if they have included 'http://' and add it if they haven't. Next we use requests to go and get the url for us, and print out the text of what is returned to the console to make sure everything is working. Finally we except any errors that are thrown and give a generic error to the user if it doesn't work. Like before we render our index.html template, however this time we include any errors and results that we have.
<br>
Run your server:
```
$ python manage.py runserver
```
You should be able now to type in a web page and in the console you'll see the text of that webpage returned.
<br>
Now we want to count the frequency of the words that are on the page and display them to the user. Update your code to the following:
```python
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from collections import Counter, OrderedDict
import os
import requests
import re
import nltk
import operator

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Result

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        #get url that the person has entered
        try:
            url = request.form['url']
            if 'http://' not in url[:7]:
                url = 'http://' + url
            r = requests.get(url)
        except:
            errors.append("Unable to get URL, please make sure it's valid and try again")
            return render_template('index.html', errors=errors)
        raw = nltk.clean_html(r.text)
        tokens = nltk.word_tokenize(raw)
        text = nltk.Text(tokens)
        nonPunct = re.compile('.*[A-Za-z].*')
        raw_words = [w for w in text if nonPunct.match(w)]
        raw_word_count = Counter(raw_words)
        stops = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
        no_stop_words = [w for w in raw_words if w.lower() not in stops]
        no_stop_words_count = Counter(no_stop_words)
        results = sorted(no_stop_words_count.items(), 
                                        key=operator.itemgetter(1),
                                        reverse=True)
        try:
            result = Result(
                    url=url,
                    result_all = raw_word_count,
                    result_no_stop_words = no_stop_words_count
                )
            db.session.add(result)
            db.session.commit()
        except:
            errors.append("Unable to add item to database")
    return render_template('index.html', errors=errors, results=results)

if __name__ == '__main__':
    app.run()
```


capture URL
convert URL
request queue for conversion
AJAXY stuff
save result
find past results based on id























