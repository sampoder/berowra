from typing import Collection
from flask import Flask, request, redirect, url_for, render_template, send_file, jsonify
from deta import Deta
from dotenv import load_dotenv
import os
import datetime
from werkzeug.utils import secure_filename
import pytz
import random
load_dotenv()

app = Flask(__name__)

deta = Deta(os.getenv("DETA_KEY"))

utc = pytz.utc

collectionsDB = deta.Base("collections")
contentDB = deta.Base("content")
drive = deta.Drive("files")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route('/', methods=["GET"])
def index():
    print(request.args.get('search'))
    items = collectionsDB.fetch({
        "title?contains": request.args.get('search')
    }if request.args.get('search') != None else {}, pages=1, buffer=50000)
    for sub_list in items:
        items = sub_list
    print(items)
    return render_template('index.html', collections=items)

@app.route("/<id>/filesJSON", methods=['GET', 'POST'])
def filesJSON(id):
    if request.method == 'POST':
        # check if the post request has the file part
        if id not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files[id]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            date = str(datetime.datetime.now(utc))
            res = drive.put(date + filename, file)
            return {'file': date + filename}
    items = drive.list()
    print(items)
    return render_template('files.html', title='Files', files=items['names'], filesPage=True, collection=False)

@app.route("/files", methods=['GET', 'POST'])
def files():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            res = drive.put(str(datetime.datetime.now(utc)) + filename, file)
            items = drive.list()
            print(items)
            return render_template('files.html', title='Files', files=items['names'])
    items = drive.list()
    print(items)
    return render_template('files.html', title='Files', files=items['names'], filesPage=True, collection=False)

@app.route("/api", methods=['GET', 'POST'])
def api():
    return render_template('api.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')


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
                finalData[int(y[0].replace('fieldTitle', '')) -
                          1]['title'] = y[1]
        for x, y in enumerate(finalData):
            print(x, y)
            finalData[x]['id'] = random.randint(0, 10000000000000)
        collectionsDB.insert({
            "title": request.form['title'],
            "templateItems": finalData,
            "lastUpdated": str(datetime.datetime.now(utc))
        })
        return redirect('/')
    else:
        return render_template('new.html')


@app.route('/collection/<id>', methods=['GET'])
def collection(id):
    data = collectionsDB.get(id)
    items = contentDB.fetch({"collectionKey": id}, pages=1, buffer=50000)
    for sub_list in items:
        items = sub_list
    print(items)
    return render_template("collection.html", title=data['title'], items=items, filesPage=False, collection=True, collectionId=id)


@app.route('/content/<id>', methods=['GET', 'POST'])
def content(id):
    if request.method == 'POST':
        formData = list(request.form.items())
        print(formData)
        contentData = contentDB.get(id)
        collectionData = collectionsDB.get(contentData['collectionKey'])
        content = contentData['content']
        if contentData['content'] == {}:
            for x in collectionData['templateItems']:
                if 'title' in x:
                    content[x['id']] = {'type': x['type'], 'title': x['title']}
        else:
            for x in collectionData['templateItems']:
                if 'title' in x and x['id'] not in content:
                    content[x['id']] = x
        title = ""
        for x in enumerate(formData):
            if x[1][0] == 'content_title':
                title = x[1][1]
            elif '-files-upload-box' in x[1][0]:
                print('skipping')
            elif '-file-checkbox-' in x[1][0]:
                content[int(x[1][0].split('-file-checkbox-')[0])]['value'] = []
                if x[1][1] == 'on':
                    if "value" in content[int(x[1][0].split('-file-checkbox-')[0])]:
                        content[int(x[1][0].split('-file-checkbox-')[0])]['value'].append(x[1][0].split('-file-checkbox-')[1])
                    else:
                        content[int(x[1][0].split('-file-checkbox-')[0])]['value'] = [x[1][0].split('-file-checkbox-')[1]]              
            else:
                content[int(x[1][0])]['value'] = x[1][1]
        contentArray = list(content.items())
        contentDB.update({'content': content, 'title': title, "lastUpdated": str(datetime.datetime.now(utc))}, id)
    getContentData = contentDB.get(id)
    getCollectionData = collectionsDB.get(getContentData['collectionKey'])
    getContent = getContentData['content']
    if getContentData['content'] == {}:
        for x in getCollectionData['templateItems']:
            if 'title' in x:
                getContent[x['id']] = {'type': x['type'], 'title': x['title']}
    else:
        for x in getCollectionData['templateItems']:
            if 'title' in x and str(x['id']) not in getContent:
                print(x)
                getContent[int(x['id'])] = x
    getContentArray = list(getContent.items())
    print(getContentArray)
    return render_template('edit.html', content=getContentArray, title=getContentData['title'])

@app.route('/collection/<id>/new', methods=['GET', 'POST'])
def newContent(id):
    res = contentDB.insert({"collectionKey": id, "content": {}, "title": "Unnamed Content"})
    print(res)
    return redirect('/content/'+res['key'])

@app.route('/api/content/<id>', methods=['GET'])
def apiContent(id):
    getContentData = contentDB.get(id)
    return jsonify(getContentData)

@app.route('/api/collection/<id>', methods=['GET'])
def apiCollection(id):
    data = collectionsDB.get(id)
    detaQuery = request.args.to_dict()
    print(detaQuery)
    detaQuery['collectionKey'] = id
    items = contentDB.fetch(detaQuery, pages=1, buffer=50000)
    for sub_list in items:
        items = sub_list
    return jsonify(items)

@app.route('/api/collections', methods=['GET'])
def apiCollections():
    detaQuery = request.args.to_dict()
    print(detaQuery)
    items = collectionsDB.fetch(detaQuery, pages=1, buffer=50000)
    for sub_list in items:
        items = sub_list
    return jsonify(items)


@app.route('/file/<id>', methods=['GET'])
def getFile(id):
    res = drive.get(id)
    return send_file(res, download_name=id)


if __name__ == "__main__":
    app.run(debug=True)
