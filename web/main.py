from flask import Flask, request, redirect, url_for, render_template
from deta import Deta
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

app = Flask(__name__)

deta = Deta(os.getenv("DETA_KEY"))

collectionsDB = deta.Base("collections")


@app.route('/', methods=["GET"])
def index():
    items = collectionsDB.fetch(pages=1, buffer=50000)
    for sub_list in items:
        items = sub_list
    return render_template('index.html', collections=items)


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        formData = list(request.form.items())
        finalData = [{}]
        for x, y in enumerate(formData):
            if 'fieldType' in y[0]:
                finalData.insert(
                    (int(y[0].replace('fieldType', '')) - 1), {'type': y[1]})
            if 'fieldTitle' in y[0]:
                finalData[int(y[0].replace('fieldTitle', '')) - 1]['title'] = y[1]
        print(finalData)
        collectionsDB.insert({
            "title": request.form['title'],
            "templateItems": [],
            "lastUpdated": str(datetime.datetime.now())
        })
        items = collectionsDB.fetch(pages=1, buffer=50000)
        for sub_list in items:
            items = sub_list
        return redirect('/')
    else:
        return render_template('new.html')


if __name__ == "__main__":
    app.run(debug=True)
