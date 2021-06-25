from flask import Flask, request, redirect, url_for, render_template
from deta import Deta
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

deta = Deta(os.getenv("DETA_KEY"))

collectionsDB = deta.Base("collections")

@app.route('/', methods=["GET"])
def hello_world():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)