from flask import Flask, request, redirect, url_for, render_template, send_file
from deta import Deta
from dotenv import load_dotenv
import os
import datetime
from werkzeug.utils import secure_filename
load_dotenv()

app = Flask(__name__)

deta = Deta(os.getenv("DETA_KEY"))

collectionsDB = deta.Base("collections")
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
            res = drive.put(filename, file)
            items = drive.list()
            print(items)
            return render_template('files.html', title='Files', files=items['names'])
    items = drive.list()
    print(items)
    return render_template('files.html', title='Files', files=items['names'])

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
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
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            res = drive.put(filename, file)
            result = drive.list()
            print(result)
            return res
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

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
        collectionsDB.insert({
            "title": request.form['title'],
            "templateItems": finalData,
            "lastUpdated": str(datetime.datetime.now())
        })
        return redirect('/')
    else:
        return render_template('new.html')


@app.route('/collection/<id>', methods=['GET'])
def collection(id):
    data = collectionsDB.get(id)
    print(data)
    return render_template("collection.html", title=data['title'])

@app.route('/file/<id>', methods=['GET'])
def getFile(id):
    res = drive.get(id)
    return send_file(res, download_name=id)


if __name__ == "__main__":
    app.run(debug=True)
