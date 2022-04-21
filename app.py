import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)
# Create a variable and an instance of Flask
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
# Configuration to grab the database name
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# Configure the actual connection string which is the Mongo URI
app.secret_key = os.environ.get("SECRET_KEY")
# Graps the secret_key

mongo = PyMongo(app)
# An instance of PyMongo using a Constructor method to add 'app' from above


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", index=index)


# @app.route("/contact", methods=["GET", "POST"])
# def contact():
#     return render_template("contact.html")


@app.route("/proctors_model")
def proctors_model():
    return render_template("proctors_model.html")


@app.route("/protecting_you")
def protecting_you():
    return render_template("protecting_you.html")


@app.route("/thecouragetobe_blog")
def thecouragetobe_blog():
    blogs = mongo.db.blogs.find()
    return render_template("blog.html", blogs=blogs)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
