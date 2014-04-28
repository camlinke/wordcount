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
We are importing render_template from flask so that we can use our newly created template. We are then changing our index route to serve that file.
<br>
Next we create a basic html template to set up our homepage:
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
We have a bit of styling to make the page not completely hideous. Then we create a form with a textbox for people to be able to enter their url.

capture URL
convert URL
request queue for conversion
AJAXY stuff
save result
find past results based on id























