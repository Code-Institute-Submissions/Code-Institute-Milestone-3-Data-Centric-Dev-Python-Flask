import os
from flask import Flask, render_template, url_for, session, request, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Connection to MongoDB Atlas
app.config["MONGO_DBNAME"] = "cookbook"
app.config["MONGO_URI"] = os.getenv('MONGODB_URI_COOKBOOK')
app.secret_key = '_5#y2L"F4Q8z\n\xec]/' #TODO this should be hidden - use os.getenv()

mongo = PyMongo(app)
bcrypt = Bcrypt(app)


@app.route("/")
@app.route("/landing_page", methods=['GET', 'POST'])
def landing_page():
   # Sign Up section
   if request.method == 'POST':
      users = mongo.db.users
      existing_user = users.find_one({"name" : request.form["username"]})

      if existing_user is None:
         hashpass = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")

         # Insert default data to mongoDB Atlas
         users.insert({
            "name" : request.form["username"],
            "password" : hashpass,
            "recipe_cards" : [
               {
               "recipe_name" : "Spaghetti Bolognese",
               "cuisine": "Italian",
               "recipe" : "Spaghetty with tomato's sauce",
               "cooked" : 0,
               "img" : "https://ichef.bbci.co.uk/food/ic/food_16x9_832/recipes/one_pot_chorizo_and_15611_16x9.jpg"
               },
               {
               "recipe_name" : "China",
               "cuisine": "Chinese",
               "recipe" : "China with chilli peppers",
               "cooked" : 0,
               "img" : "https://www.intrepidtravel.com/sites/intrepid/files/styles/low-quality/public/elements/product/hero/RFA-heroes_0012_china_chengdu_IMG_6454.jpg"
               }
               ]
            })
         return redirect(url_for("login"))
      
      return "The username already exist!"

   return render_template("landing.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      users = mongo.db.users
      login_user = users.find_one({"name" : request.form["username"]})
   
      if login_user:
         if bcrypt.check_password_hash(login_user["password"].encode('utf-8'), request.form["password"]):
            session["username"] = request.form["username"]
            return redirect(url_for("main_page", username=session["username"]))
         return "Invalid username/password combination"
      return "Invalid username"
   
   return render_template("login.html")


@app.route("/main_page")
def main_page():
   users = mongo.db.users
   login_user = users.find_one({"name" : request.args.get("username", None)})

   return render_template("main_page.html", user=login_user)


@app.route("/main_page/add_cookcard/")
def add_page():
   return render_template("add_cookcard.html")

if __name__ == '__main__':
   app.run(debug=True)

'''
host=os.environ.get('IP'), port=int(os.environ.get('PORT')),
'''