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

      # Verifying users if they have an account
      if login_user:

         # If user exist in database then check password
         if bcrypt.check_password_hash(login_user["password"].encode('utf-8'), request.form["password"]):
            session["username"] = request.form["username"]

            # If login & password matches then redirect user to main page, otherwise pop out errors
            if "username" in session:
               return redirect(url_for("main_page", username=session["username"]))

         return "Invalid username/password combination"
      return "Invalid username"
   
   return render_template("login.html")


@app.route("/main_page/<username>")
def main_page(username):
   users = mongo.db.users
   login_user = users.find_one({"name" : username})

   return render_template("main_page.html", user=login_user)


@app.route("/main_page/<username>/add_cookcard", methods=['GET', 'POST'])
def add_page(username):
   if request.method == 'POST':
      users = mongo.db.users

      # Update mongoDB Atlas by a new food card
      users.update( {"name": username},
      {
         "$push": {"recipe_cards": {
            "recipe_name" : request.form["recipe_name"],
            "cuisine": request.form["cuisine"],
            "recipe" : request.form["recipe"],
            "cooked" : 0,
            "img" : request.form["upload_picture"]
            }
         }
      })

      return redirect(url_for("main_page", username=session["username"]))

   return render_template("add_cookcard.html")


@app.route("/main_page/<username>/edit_cookcard/<recipe_name>", methods=['GET', 'POST'])
def edit_page(username, recipe_name):

   # It returns just one object in array of recipe_cards
   foodcard = mongo.db.users.find_one({
      "name": username,
   },
      {"recipe_cards": {"$elemMatch": {"recipe_name": recipe_name}} }
   )

   """
   THIS IS FOR UPDATE SECTION

   user = mongo.db.users.update(
      {
         "name": username,
         "recipe_cards.recipe_name": recipe_name
      },
      {
         "$set": {
            "recipe_cards.$.recipe_name": "FUNGUJE TOOOO"
         }
      }
   )
   """
   return render_template("edit_cookcard.html", foodcard=foodcard["recipe_cards"][0])


if __name__ == '__main__':
   app.run(debug=True)

'''
host=os.environ.get('IP'), port=int(os.environ.get('PORT')),
'''