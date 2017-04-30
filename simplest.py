from flask import Flask, render_template, send_from_directory, abort, request, session, redirect, send_file, url_for, jsonify
import flask
import json
import os
import random

app = Flask(__name__, static_url_path='')
api_key = "0000000000000000"

# Configuration
app_name = "i.noku.space"
host = "localhost"
port = 1124


@app.route("/")
def index():
    return render_template("index.html", app_name=app_name)


@app.route("/upload",  methods=["POST"])
def upload():
    """
    Post data requires the files under 'images' and the API Key in 'api_key'
    """
    if request.method == "POST":
        for x in request.form.keys():
            print("{0}: {1}".format(x, request.form[x]))
        f = request.files['images']

        if request.form["api_key"] != api_key:
            return jsonify({"status" : 100, "error" : "Invalid API Key"})
        
        print("Saving to: " + f.filename)
        f.save("images\\" + f.filename)
        path = url_for("sendImage", img_path=f.filename)
        path = request.url_root + path[1:]
        return jsonify({"status" : 200, "url" : path})

@app.route("/a/<img_path>")
def sendImage(img_path):
    if not os.path.isfile("images\\"+img_path):
        abort(404)
    return send_from_directory('images', img_path)


@app.errorhandler(404)
def err_404(e):
    return render_template("noimg.html", app_name=app_name)

if __name__ == "__main__":
    
    try:
        # Tries loading the API Key
        with open("api_key", "r") as f:
            api_key = f.read()
    except:
        # Generates an API Key.
        api_key = "".join([random.choice("1234567890abcdef") for x in range(0, 16)])
        with open("api_key", "w") as f:
            f.write(api_key)

    print("api_key is {0}".format(api_key))
    app.run(host=host, port=port)