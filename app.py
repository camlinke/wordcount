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
            print "didn't work"
    return render_template('index.html', errors=errors, results=results)

if __name__ == '__main__':
    app.run()