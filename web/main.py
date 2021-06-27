from flask import Flask, request, redirect, url_for, render_template
from deta import Deta
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

deta = Deta(os.getenv("DETA_KEY"))

collectionsDB = deta.Base("collections")

@app.route('/', methods=["GET"])
def index():
    items = collectionsDB.fetch(pages=1, buffer=50000)
    for sub_list in items: 
        items = sub_list
    print(items)
    return render_template('index.html', collections=items)

@app.route('/new', methods=["GET"])
def new():
    collectionsDB.insert({
        "title": "Blog Posts",
        "templateItems": [],
        "description": "Blogs to be posted on sampoder.com"
    })
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)