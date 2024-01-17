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
@app.route("/index", methods=["POST, GET"])
def index():
    return render_template("index.html", index=index)


@app.route("/proctors_model")
def proctors_model():
    return render_template("proctors_model.html")


@app.route("/protecting_you")
def protecting_you():
    return render_template("protecting_you.html")


@app.route("/thecouragetobe_blog")
def thecouragetobe_blog():
    blogs = list(
        mongo.db.blogs.find().sort("_id", -1))
    return render_template("blog.html", blogs=blogs)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username already exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        # If the username already exists a message is displayed to the user
        if existing_user:
            # Takes the user back to the register form to try again
            return redirect(url_for("register"))

        # Else statement using a dictionary
        register = {
            # Username in parentheses is from the name attr in reg template
            "username": request.form.get("username").lower(),
            # Password in parentheses is from the name attr in reg template
            # Werkzeug security helper used below
            "password": generate_password_hash(request.form.get("password"))
        }
        # Calling the function using the insert_one method
        mongo.db.users.insert_one(register)

        # Put the new user into 'session' cookie
        session['user'] = request.form.get("username").lower()
        return redirect(url_for("blog_admin",
                                username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if username already exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Ensure password matches user input
            # check_password_hash from Werkzeug
            # Had to use 2 space indenting for PEP8 compliance
            if check_password_hash(
              existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("blog_admin",
                                        username=session["user"]))
            else:
                # Invalid password match message to user
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # Username doesn't exist message to user
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    # Returns user to main login page to try again
    return render_template("login.html")


@app.route("/blog_admin/", methods=["GET", "POST"])
def blog_admin():
    # Only users can access their own profile
    if not session.get("user"):
        return render_template("blog.html")

    # Grabs the session user's username from the database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        # Admin only can access all
        if session["user"] == "brian":
            blogs = list(mongo.db.blogs.find().sort("_id", -1))
        else:
            # Logged in users will see just their own posts
            blogs = list(
                mongo.db.blogs.find(
                    {"created_by": session["user"]}).sort("_id", -1))
        return render_template(
            "blog_admin.html", username=username, blogs=blogs)
    return redirect(url_for("login"))


# Function for user to logout
@app.route("/logout")
def logout():
    # Remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        # Dictionary created and assigned to 'post'
        post = {
            "category_name": request.form.get("category_name"),
            "blog_name": request.form.get("blog_name"),
            "blog_details": request.form.get("blog_details"),
            "blog_details_2": request.form.get("blog_details_2"),
            "blog_details_3": request.form.get("blog_details_3"),
            "blog_details_4": request.form.get("blog_details_4"),
            "blog_details_5": request.form.get("blog_details_5"),
            "blog_details_6": request.form.get("blog_details_6"),
            "blog_details_7": request.form.get("blog_details_7"),
            "blog_details_8": request.form.get("blog_details_8"),
            "blog_details_9": request.form.get("blog_details_9"),
            "publish_date": request.form.get("publish_date"),
            "created_by": session["user"]
        }
        mongo.db.blogs.insert_one(post)
        flash("Post Added Successfully")
        return redirect(url_for("blog_admin"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_post.html", categories=categories)


@app.route("/edit_post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if request.method == "POST":
        edit = {
            "category_name": request.form.get("category_name"),
            "blog_name": request.form.get("blog_name"),
            "blog_details": request.form.get("blog_details"),
            "blog_details_2": request.form.get("blog_details_2"),
            "blog_details_3": request.form.get("blog_details_3"),
            "blog_details_4": request.form.get("blog_details_4"),
            "blog_details_5": request.form.get("blog_details_5"),
            "blog_details_6": request.form.get("blog_details_6"),
            "blog_details_7": request.form.get("blog_details_7"),
            "blog_details_8": request.form.get("blog_details_8"),
            "blog_details_9": request.form.get("blog_details_9"),
            "publish_date": request.form.get("publish_date"),
            "created_by": session["user"]
        }
        mongo.db.blogs.update_one({"_id": ObjectId(post_id)}, {"$set": edit})
        flash("Post Updated Successfully")
        return redirect(url_for("blog_admin", username=session["user"]))

    post = mongo.db.blogs.find_one({"_id": ObjectId(post_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_post.html", post=post, categories=categories)


@app.route("/delete_post/<post_id>")
def delete_post(post_id):
    mongo.db.blogs.delete_one({"_id": ObjectId(post_id)})
    flash("Post Successfully Removed")
    return redirect(url_for("blog_admin", username=session["user"]))


@app.route("/categories")
def categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


@app.route("/add_categories", methods=["GET", "POST"])
def add_categories():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.insert_one(category)
        flash("New Category Added")
        return redirect(url_for("add_post"))

    return render_template("add_categories.html")


@app.route("/edit_categories/<category_id>", methods=["GET", "POST"])
def edit_categories(category_id):
    if request.method == "POST":
        change = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.update_one({"_id": ObjectId(category_id)},
                                       {"$set": change})
        flash("Category Name Successfully Changed")
        return redirect(url_for("add_post"))

    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_categories.html", category=category)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.categories.delete_one({"_id": ObjectId(category_id)})
    flash("Category Successfully Deleted")
    return redirect(url_for("add_post"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
