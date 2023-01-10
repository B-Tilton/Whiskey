from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_app.models.user import users
from flask_app.models.whiskey import whiskey

@app.route("/new_whiskey")
def new_whiskey():
    if "id" not in session:
        return redirect("/home")
    return render_template("new_whiskey.html")

@app.route("/save_whiskey", methods = ["POST"])
def save_whiskey():
    if "id" not in session:
        return redirect("/home")
    if whiskey.valid_whiskey(request.form) != True:
        return redirect("/new_whiskey")
    data = {
        "name": request.form["name"],
        "distiller": request.form["distiller"],
        "malt": request.form["malt"],
        "abv": request.form["abv"],
        "rating": request.form["rating"],
        "date_tasted": request.form["date_tasted"],
        "user_id":request.form["user_id"]
    }
    print(data)
    whiskey.save_whiskey(data)
    return redirect("/whiskeys/{id}")

@app.route("/view_whiskey/<id>")
def veiw_one(id):
    if "id" not in session:
        return redirect("/home")
    data = {"id" : id}
    return render_template("view_whiskey.html", whiskey = whiskey.one_whiskey_with_creator(data))

@app.route("/edit_whiskey/<id>")
def edit_whiskey(id):
    if "id" not in session:
        return redirect("/home")
    data = {"id": id}
    one_whiskey = whiskey.get_one_whiskey(data)
    return render_template("edit_whiskey.html", whiskey = one_whiskey)

@app.route("/update_whiskey", methods = ["POST"])
def update_whiskey():
    if "id" not in session:
        return redirect("/home")
    print(request.form)
    print(session["id"])
    if whiskey.valid_whiskey(request.form) != True:
        return redirect(f'/edit_whiskey/{request.form["whiskey_id"]}')
    whiskey.update_whiskey(request.form)
    return redirect(f'/whiskeys/{session["id"]}')

@app.route("/delete/<id>")
def delete(id):
    data = {"id" : id}
    whiskey.delete(data)
    return redirect(f'/whiskeys/{session["id"]}')