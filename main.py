from typing import Collection
from flask import Flask, request, redirect, url_for, render_template, send_file, jsonify, make_response
from deta import Deta
from dotenv import load_dotenv
import os
import datetime
from werkzeug.utils import secure_filename
import pytz
import random
load_dotenv()

path = "" if os.getenv("LOCAL_DEV") else "https://" + os.getenv("DETA_PATH")
host = ".deta.app" if os.getenv("DETA_SPACE_APP") else "" if os.getenv(
    "LOCAL_DEV") else ".deta.dev"

app = Flask(__name__)

deta = Deta()

utc = pytz.utc

collectionsDB = deta.Base("collections")
contentDB = deta.Base("content")
drive = deta.Drive("files")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route('/', methods=["GET"])
def index():
    print(request.args.get('search'))
    items = collectionsDB.fetch({
        "titleCaps?contains": request.args.get('search').upper()
    }if request.args.get('search') != None and request.args.get('search').replace(' ', '') != '' else {}, pages=1, buffer=50000)
    for sub_list in items:
        items = sub_list
    print(items)
    r = make_response(render_template('index.html', collections=items, searchPlaceholder=request.args.get(
        'search')if request.args.get('search') != None and request.args.get('search').replace(' ', '') != '' else 'Filter results'))
    r.headers.set('cache-control', 'no-store')
    return r


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
            res = drive.put(date.replace(' ', '') + filename, file)
            return {'file': date.replace(' ', '') + filename}
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
            res = drive.put(str(datetime.datetime.now(
                utc)).replace(' ', '') + filename, file)
            items = drive.list()
            print(items)
            return render_template('files.html', title='Files', files=items['names'])
    items = drive.list()
    if request.args.get('search') != None and request.args.get('search').replace(' ', '') != '':
        print(items)
        items = {'names': [a for a in items['names']
                           if request.args.get('search').upper() in a.upper()]}
        print(items)
    return render_template('files.html', title='Files', files=items['names'], filesPage=True, collection=False, searchPlaceholder=request.args.get('search')if request.args.get('search') != None and request.args.get('search').replace(' ', '') != '' else 'Filter results')


@app.route("/api", methods=['GET', 'POST'])
def api():
    items = collectionsDB.fetch({}, pages=1, buffer=50000)
    for sub_list in items:
        items = sub_list
    try:
        contentItems = contentDB.fetch(
            {"collectionKey": items[0]["key"]}, pages=1, buffer=50000)
        print(contentItems)
        for sub_list in contentItems:
            contentItems = sub_list
    except:
        contentItems = []
    print(contentItems)
    return render_template('api.html', collections=items, exampleKey=contentItems[0]['key'] if len(contentItems) > 0 else None)


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
            "titleCaps": request.form['title'].upper(),
            "templateItems": finalData,
            "lastUpdated": str(datetime.datetime.now(utc))
        })
        return redirect(f"{path}{host}/")
    else:
        return render_template('new.html')


@app.route('/collection/<id>', methods=['GET'])
def collection(id):
    data = collectionsDB.get(id)
    items = contentDB.fetch({"collectionKey": id,
                             "titleCaps?contains": request.args.get('search').upper()
                             }if request.args.get('search') != None and request.args.get('search').replace(' ', '') != '' else {"collectionKey": id}, pages=1, buffer=50000)
    for sub_list in items:
        items = sub_list
    print(items)
    return render_template("collection.html", title=data['title'], items=items, filesPage=False, collection=True, collectionId=id, searchPlaceholder=request.args.get('search')if request.args.get('search') != None and request.args.get('search').replace(' ', '') != '' else 'Filter results', collectionIdDisplay='('+id+')')


@app.route('/collection/<id>/edit', methods=['GET'])
def collectionEdit(id):
    data = collectionsDB.get(id)
    return render_template("editCollection.html", title=data['title'], collectionId=id, collectionIdDisplay='('+id+')', collectionItems = data['templateItems'])


@app.route('/collection/<id>/edit/new-field', methods=['POST'])
def collectionAddField(id):
    data = collectionsDB.get(id)
    print(data['templateItems'])
    data['templateItems'].append({
        "id": random.randint(0, 10000000000000),
        "title": request.form['fieldTitle'],
        "type": request.form['fieldType']
    })
    collectionsDB.put(data)
    return redirect(f"{path}{host}/collection/"+id+"/edit")

@app.route('/collection/<id>/edit/edit-field/<field>', methods=['POST'])
def collectionEditField(id, field):
    data = collectionsDB.get(id)
    for templateItemIndex, templateItem in enumerate(data['templateItems']):
        if int(templateItem['id']) == int(field):
            data['templateItems'][templateItemIndex] = {
                "id": int(field),
                "title": request.form['fieldTitle'],
                "type": request.form['fieldType']
            }
    collectionsDB.put(data)
    return redirect(f"{path}{host}/collection/"+id+"/edit")

@app.route('/collection/<id>/edit/delete-field/<field>', methods=['GET'])
def collectionDeleteField(id, field):
    data = collectionsDB.get(id)
    for templateItemIndex, templateItem in enumerate(data['templateItems']):
        if int(templateItem['id']) == int(field):
            del data['templateItems'][templateItemIndex]
    collectionsDB.put(data)
    return redirect(f"{path}{host}/collection/"+id+"/edit")

@app.route('/collection/<id>/delete', methods=['GET'])
def collectionDelete(id):
    collectionsDB.delete(id)
    return redirect(f"{path}{host}/")


@app.route('/content/<id>/delete', methods=['GET'])
def contentDelete(id):
    contentData = contentDB.get(id)
    contentDB.delete(id)
    return redirect(f"{path}{host}/collection/"+contentData['collectionKey'])


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
        published = False
        for x in enumerate(formData):
            if x[1][0] == 'content_title':
                title = x[1][1]
            elif x[1][0] == 'published-checkbox':
                published = True
            elif '-files-upload-box' in x[1][0]:
                print('skipping')
            elif '-file-checkbox-' in x[1][0]:
                content[int(x[1][0].split('-file-checkbox-')[0])]['value'] = []
                if x[1][1] == 'on':
                    if "value" in content[int(x[1][0].split('-file-checkbox-')[0])]:
                        content[int(x[1][0].split('-file-checkbox-')[0])
                                ]['value'].append(x[1][0].split('-file-checkbox-')[1])
                    else:
                        content[int(x[1][0].split('-file-checkbox-')[0])
                                ]['value'] = [x[1][0].split('-file-checkbox-')[1]]
            elif content[int(x[1][0])]["type"] == 'String Array':
                content[int(x[1][0])]['value'] = x[1][1].split(',')
            else:
                content[int(x[1][0])]['value'] = x[1][1]
        contentArray = list(content.items())
        contentDB.update({'content': content, 'published': published, 'title': title, 'titleCaps': title.upper(),
                         "lastUpdated": str(datetime.datetime.now(utc))}, id)
        return redirect(f"{path}{host}/collection/{contentData['collectionKey']}")
    getContentData = contentDB.get(id)
    getCollectionData = collectionsDB.get(getContentData['collectionKey'])
    getContent = getContentData['content']
    templateItemsKeys = []
    for x in getCollectionData['templateItems']:
        print()
        templateItemsKeys.append(str(x['id']))
    if getContentData['content'] == {}:
        print('hi!')
        for x in getCollectionData['templateItems']:
            print(x)
            if 'title' in x:
                getContent[str(x['id'])] = {'type': x['type'], 'title': x['title']}
    else:
        for x in getCollectionData['templateItems']:
            print(x)
            if 'title' in x and str(x['id']) not in getContent:
                print(x)
                print('test:')
                print(x)
                getContent[int(x['id'])] = x
            elif 'title' in x and str(x['id']) in getContent:
                x['value'] = getContent[str(x['id'])]['value'] if 'value' in getContent[str(x['id'])] else ''
                getContent[str(x['id'])] = x
    for x in list(getContent):
        print(x)
        if str(x) not in templateItemsKeys:
            print('deleting:')
            print(x)
            del getContent[x]
    getContentArray = list(getContent.items())
    return render_template('edit.html', content=getContentArray, title=getContentData['title'], published="checked"if getContentData['published'] == True else "", contentId=id)


@app.route('/collection/<id>/new', methods=['GET', 'POST'])
def newContent(id):
    res = contentDB.insert(
        {"collectionKey": id, "content": {}, "title": "Unnamed Content", "published": False, "lastUpdated": str(datetime.datetime.now(utc))})
    print(res)
    return redirect(f"{path}{host}/content/" + res['key'])


@app.route('/api/content/<id>', methods=['GET'])
def apiContent(id):
    getContentData = contentDB.get(id)
    return jsonify({
        "collectionKey": getContentData["collectionKey"],
        "content": getContentData["content"],
        "lastUpdated": getContentData["lastUpdated"],
        "title": getContentData["title"]
    })


@app.route('/api/collection/<id>', methods=['GET'])
def apiCollection(id):
    includeContent = False

    def formatItem(n):
        return {"key": n["key"],
                "lastUpdated": n["lastUpdated"],
                "title": n['title']} if includeContent == False else {"key": n["key"],
                                                                      "lastUpdated": n["lastUpdated"],
                                                                      "title": n['title'], 'content': n['content']}
    data = collectionsDB.get(id)
    providedDetaQuery = request.args.to_dict()
    detaQuery = {}
    for x in providedDetaQuery:
        detaQuery[x.replace('!', '?')] = providedDetaQuery[x]
    detaQuery['collectionKey'] = id
    detaQuery['published'] = True
    if 'content' in detaQuery:
        includeContent = True
    detaQuery.pop('content', None)
    items = contentDB.fetch(detaQuery, pages=1, buffer=50000)
    for sub_list in items:
        items = sub_list
    return jsonify({"title": data["title"], "items": list(map(formatItem, items))})


@app.route('/api/collections', methods=['GET'])
def apiCollections():
    includeTemplate = False

    def formatItem(n):
        return {"key": n["key"],
                "lastUpdated": n["lastUpdated"],
                "title": n['title']} if includeTemplate == False else {"key": n["key"],
                                                                       "lastUpdated": n["lastUpdated"],
                                                                       "title": n['title'], 'templateItems': n['templateItems']}
    providedDetaQuery = request.args.to_dict()
    detaQuery = {}
    for x in providedDetaQuery:
        detaQuery[x.replace('!', '?')] = providedDetaQuery[x]
    if 'template' in detaQuery:
        includeTemplate = True
    detaQuery.pop('template', None)
    print(detaQuery)
    items = collectionsDB.fetch(detaQuery, pages=1, buffer=50000)
    for sub_list in items:
        items = sub_list
    return jsonify(list(map(formatItem, items)))


@app.route('/file/<id>', methods=['GET'])
def getFile(id):
    res = drive.get(id)
    return send_file(res, download_name=id)


if __name__ == "__main__":
    app.run(debug=True)
