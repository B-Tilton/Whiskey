
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user
from flask import flash

class whiskey:
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.distiller = data["distiller"]
        self.malt = data["malt"]
        self.abv = data["abv"]
        self.rating = data["rating"]
        self.user_id = data["user_id"]
        self.date_tasted = data["date_tasted"]
        self.creator = None

    @classmethod
    def save_whiskey(cls,data):
        query = "INSERT INTO whiskey (name, distiller, malt, abv, rating, date_tasted, user_id) VALUES (%(name)s, %(distiller)s, %(malt)s, %(abv)s, %(rating)s, %(date_tasted)s, %(user_id)s);"
        return connectToMySQL("whiskey").query_db(query,data)

    @classmethod
    def whiskey_from_user(cls,data):
        query = "SELECT * FROM whiskey.whiskey JOIN whiskey.user On whiskey.user_id = user.id WHERE user_id = %(id)s ORDER BY whiskey.date_tasted DESC"
        results = connectToMySQL("whiskey").query_db(query,data)
        whiskeys = []
        print(results)
        for row in results:
            one_whiskey = cls(row)
            whiskey_creator = {
                "id" : row["user.id"],
                "fname" : row["fname"],
                "lname" : row["lname"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at": row["created_at"]
            }
            creator = user.users(whiskey_creator)
            one_whiskey.creator = creator
            whiskeys.append(one_whiskey)
        return whiskeys

    @classmethod
    def get_one_whiskey(cls,data):
        query = "SELECT * FROM whiskey.whiskey WHERE id = %(id)s"
        results = connectToMySQL("whiskey").query_db(query,data)
        return cls(results[0])

    @classmethod
    def one_whiskey_with_creator(cls,data):
        query = "SELECT * FROM whiskey.whiskey JOIN whiskey.user On whiskey.user_id = user.id WHERE whiskey.id = %(id)s ORDER BY whiskey.date_tasted DESC"
        results = connectToMySQL("whiskey").query_db(query,data)
        whiskeys = []
        print(results)
        for row in results:
            one_whiskey = cls(row)
            whiskey_creator = {
                "id" : row["user.id"],
                "fname" : row["fname"],
                "lname" : row["lname"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at": row["created_at"]
            }
            creator = user.users(whiskey_creator)
            one_whiskey.creator = creator
            whiskeys.append(one_whiskey)
        return whiskeys[0]
        
    @classmethod
    def whiskey_from_others(cls,data):
        query = "SELECT * FROM whiskey.whiskey JOIN whiskey.user On whiskey.user_id = user.id WHERE whiskey.user_id != %(id)s "
        results = connectToMySQL("whiskey").query_db(query,data)
        whiskeys = []
        print(results)
        for row in results:
            one_whiskey = cls(row)
            whiskey_creator = {
                "id" : row["user.id"],
                "fname" : row["fname"],
                "lname" : row["lname"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at": row["created_at"]
            }
            creator = user.users(whiskey_creator)
            one_whiskey.creator = creator
            whiskeys.append(one_whiskey)
        return whiskeys

    @classmethod
    def update_whiskey(cls,data):
        query = "UPDATE whiskey.whiskey SET name = %(name)s, distiller = %(distiller)s, malt = %(malt)s, abv = %(abv)s, rating = %(rating)s, date_tasted = %(date_tasted)s WHERE id = %(whiskey_id)s"
        return connectToMySQL('whiskey').query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM whiskey.whiskey WHERE id = %(id)s"
        return connectToMySQL('whiskey').query_db(query,data)

    @staticmethod
    def valid_whiskey(whiskey):
        valid = True
        if len(whiskey["name"]) < 2:
            flash("Name Must Be More Than 2 Characters")
            valid = False
        if len(whiskey["distiller"]) < 2:
            flash("Distiller Must Be More Than 4 Characters")
            valid = False
        if whiskey["malt"] == "":
            flash("Missing Malt Type")
            valid = False
        if len(whiskey["abv"]) < 2:
            flash("ABV Must Be More Tha 2 Characters")
            valid = False
        if whiskey["rating"] == "":
            flash("Missing Rating")
            valid = False
        if whiskey["date_tasted"] == "":
            flash("Missing Date")
            valid = False
        return valid