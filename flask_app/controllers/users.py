from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_app.models.user import users
from flask_app.models.whiskey import whiskey
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return redirect("/home")

@app.route("/home")
def register():
    return render_template("log_reg.html")

@app.route("/register", methods = ["POST"])
def save():
    if users.valid_reg(request.form) != True:
        return redirect("/home")
    if users.show_email(request.form):
        flash("Account With This Email Already Exists", "reg")
        return redirect("/home")
    hash = bcrypt.generate_password_hash(request.form["password"])
    print(hash)
    data = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"],
        "password": hash
    }
    print(data)
    id = users.save(data)
    session['id'] = id
    return redirect(f"/whiskeys/{id}")

@app.route("/login", methods = ["POST"])
def login():
    user = users.show_email(request.form)
    if user == False:
        flash("Invalid Email/Password", "log")
        return redirect("/home")
    if bcrypt.check_password_hash(user.password, request.form["password"]) == False:
        flash("Invalid Email/Password", "log")
        return redirect("/home")
    session["id"] = user.id
    return redirect(f"/whiskeys/{user.id}")

@app.route("/whiskeys/<id>")
def show_recipes(id):
    if "id" not in session:
        return redirect("/home")
    data = {"id":session["id"]}
    return render_template("whiskey.html", user = users.show_id(data), whiskeys = whiskey.whiskey_from_user(data), other_whiskeys = whiskey.whiskey_from_others(data))
    

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/home")