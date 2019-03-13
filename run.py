import os
from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Connection to MongoDB Atlas
app.config["MONGO_DBNAME"] = "cookbook"
app.config["MONGO_URI"] = os.getenv('MONGODB_URI_COOKBOOK')

mongo = PyMongo(app)


@app.route("/")
@app.route("/landing_page")
def landing_page():
   return render_template("landing.html", recipe_cards=mongo.db.recipe_cards.find())


@app.route("/log_in")
def log_in():
   return render_template("login.html")

if __name__ == '__main__':
   app.run(debug=True)

'''
host=os.environ.get('IP'), port=int(os.environ.get('PORT')),
'''