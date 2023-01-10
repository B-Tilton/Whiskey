from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.whiskey import whiskey
from flask import flash
import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z0-9]+$')
pass_regex = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$')
class users:
    def __init__(self,data):
        self.id = data["id"]
        self.fname = data["fname"]
        self.lname = data["lname"]
        self.email = data["email"]
        self.password = data["password"]
        self.recipes = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO whiskey.user (fname, lname, email, password) VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s);"
        return connectToMySQL("whiskey").query_db(query, data)

    @classmethod
    def show_id(cls,data):
        query  = "SELECT * FROM whiskey.user WHERE id = %(id)s;"
        result = connectToMySQL('whiskey').query_db(query,data)
        print(result)
        return cls(result[0])

    @classmethod
    def show_email(cls,data):
        query = "SELECT * FROM whiskey.user WHERE email = %(email)s;"
        results = connectToMySQL("whiskey").query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])
    
    @staticmethod
    def valid_reg(user_reg):
        valid = True
        if len(user_reg["fname"]) < 2:
            flash("First Name Must Be More Than 2 Characters","reg")
            valid = False
        if len(user_reg["lname"]) < 2:
            flash("Last Name Must Be More Than 2 Characters","reg")
            valid = False
        if not email_regex.match(user_reg["email"]):
            flash("Please Enter A Valid Email")
            valid = False
        if not pass_regex.match(user_reg["password"]):
            flash("Password Must Be At Least 8 Characters And Contain 1 Uppercase, 1 Lowercase and 1 Number", "reg")
            valid = False
        if user_reg["password"] != user_reg["re_password"]:
            flash("Passwords Don't Match", "reg")
            valid = False
        return valid

