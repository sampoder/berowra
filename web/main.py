from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello_world():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)