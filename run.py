import os
from flask import Flask, render_template, url_for, session, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Connection to MongoDB Atlas
app.config["MONGO_DBNAME"] = "cookbook"
app.config["MONGO_URI"] = os.getenv('MONGODB_URI_COOKBOOK')

mongo = PyMongo(app)


@app.route("/")
@app.route("/landing_page", methods=['GET', 'POST'])
def landing_page():
   if request.method == 'POST':
      users = mongo.db.users
      print(request.form["username"])
      existing_user = users.find_one({"name" : request.form["username"]})

      #if existing_user is None:
      #  hashpass = Bcrypt.hashpw(request.form["password"])


   return render_template("landing.html", recipe_cards=mongo.db.recipe_cards.find())


@app.route("/login")
def login():
   if "username" in session:
      return "You are logged in as " + session["username"]

   return render_template("login.html")


if __name__ == '__main__':
   app.run(debug=True)

'''
host=os.environ.get('IP'), port=int(os.environ.get('PORT')),
'''