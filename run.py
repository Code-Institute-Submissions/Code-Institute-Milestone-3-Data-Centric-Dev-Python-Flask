import os, math
from flask import Flask, render_template, url_for, session, request, redirect, jsonify, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask import send_from_directory
from random import randint


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

# Connection to MongoDB Atlas
app.config["MONGO_DBNAME"] = "cookbook"
app.config["MONGO_URI"] = os.getenv('MONGODB_URI_COOKBOOK')
app.secret_key = '_5#y2L"F4Q8z\n\xec]/' #TODO this should be hidden - use os.getenv()

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_pagination(user, username, current_page):
   # Return to the same page where the card was
   # Get length of recipecards array in order to create pagination
   login_user_len = user.find_one({"name" : username})

   # Get lenght of recipecards
   length_pagination = len(login_user_len["recipe_cards"])

   # Number of paginatoion needed
   pages = math.ceil(length_pagination / 5)

   offset = 0
   clicked_page = 0

   # If initial render 
   if current_page == -1:

      limit = 5
      # Show only 5 recipe cards on the page
      show_cards = user.find_one(
         {"name" : username},
            
         {"recipe_cards": {"$slice": [offset, limit]}}
      )

      return render_template("main_page.html", user=show_cards, pages=pages, clicked_page=clicked_page)

   else:      
      if request.method == "POST":

         number = current_page

         # -1 because of indexing (page 1 has index 0)
         clicked_page = number - 1

         if number == 1:
            offset = number - 1
               
         elif number == 2:
            offset = 5

         elif number > 2:
            offset = 5 * (number - 1)

      limit = 5

      # Show only 5 recipe cards on the page
      show_cards = user.find_one(
         {"name" : username},
               
         {"recipe_cards": {"$slice": [offset, limit]}}
      )

      return render_template("main_page.html", user=show_cards, pages=pages, clicked_page=clicked_page)



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
                     "recipe_id": randint(1,1000000),
                     "recipe_name" : "Spaghetti Bolognese",
                     "cuisine": "Italian",
                     "recipe" : "<p>Spaghetty with tomato's sauce</p>",
                     "cooked" : int(0),
                     "img" : "empty"
                  }
               ]
            })

         return redirect(url_for("login"))

      return jsonify({"error": request.form["username"] + " already exists!"})

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

      flash("Invalid username/password combination") 
   
   return render_template("login.html")


@app.route("/main_page/<username>", methods=['GET', 'POST'])
def main_page(username):
   users = mongo.db.users
   # -1 for initial render
   current_page = -1

   if request.method == "POST":
      current_page = int(request.form["page_number"])
   

   return get_pagination(users, username, current_page)

@app.route("/main_page_query/<username>", methods=['GET', 'POST'])
def main_page_query(username):
   users = mongo.db.users
   
   # Sorting cards based on name, cusiene or hearts
   if request.method == 'POST':
      sort_by = request.form["sort"]
      
      if sort_by == "name":
         # Sorting by name of food
         users.update(
            { "name": username},
            {
               "$push": {
                  "recipe_cards": {
                     "$each": [],
                     "$sort": { "recipe_name": 1 }
                  }
               }
            }
         )
      elif sort_by == "cuisine":
         # Sorting by cuisine
         users.update(
            { "name": username},
            {
               "$push": {
                  "recipe_cards": {
                     "$each": [],
                     "$sort": { "cuisine": 1 }
                  }
               }
            }
         )
      else:
         # Sorting by cooked number
         users.update(
            { "name": username},
            {
               "$push": {
                  "recipe_cards": {
                     "$each": [],
                     "$sort": { "cooked": -1 }
                  }
               }
            }
         )
      
   return redirect(url_for("main_page", username=session["username"]))

@app.route("/main_page/<username>/add_cookcard", methods=['GET', 'POST'])
def add_page(username):
   if request.method == 'POST':
      users = mongo.db.users

      # Upload images
      if "upload_picture" in request.files:
         file = request.files['upload_picture']

         if not allowed_file(file.filename):
            #TODO do it in better way when the extantion is not allowed
            return "extenstion is not allowed"

         if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Create a unique name file
            change_filename = request.form["recipe_name"] + "_" + request.form["cuisine"] + "_" + filename

            mongo.save_file(change_filename, file)

            # Update mongoDB Atlas by a new food card
            users.update( {"name": username},
            {
               "$push": {"recipe_cards": {
                  "recipe_id": randint(1,1000000),
                  "recipe_name" : request.form["recipe_name"].capitalize(),
                  "cuisine": request.form["cuisine"].capitalize(),
                  "recipe" : request.form["recipe"],
                  "cooked" : int(0),
                  "img" : change_filename
                  }
               }
            })
      else:
         users.update( {"name": username},
               {
                  "$push": {"recipe_cards": {
                     "recipe_id": randint(1,1000000),
                     "recipe_name" : request.form["recipe_name"].capitalize(),
                     "cuisine": request.form["cuisine"].capitalize(),
                     "recipe" : request.form["recipe"],
                     "cooked" : int(0),
                     "img" : "empty"
                     }
                  }
               })

      return redirect(url_for("main_page", username=session["username"]))

   return render_template("add_cookcard.html")


@app.route("/file/<filename>")
def file(filename):
   return mongo.send_file(filename)


@app.route("/main_page/<username>/edit_cookcard/<recipe_name>", methods=['GET', 'POST'])
def edit_page(username, recipe_name):

   # It returns just one object in array of recipe_cards
   cookcard = mongo.db.users.find_one({
      "name": username,
   },
      {"recipe_cards": {"$elemMatch": {"recipe_name": recipe_name}} }
   )

   return render_template("edit_cookcard.html", cookcard=cookcard["recipe_cards"][0] )

@app.route("/main_page/<username>/update_foodcard/<recipe_name>/<recipe_img>/", methods=['GET', 'POST'])
def update_cookcard(username, recipe_name, recipe_img):
   if request.method == 'POST':
      user = mongo.db.users

      # Upload images
      if "upload_picture" in request.files:
         file = request.files['upload_picture']

         if not allowed_file(file.filename):
            #TODO do it in better way when the extantion is not allowed
            return "extenstion is not allowed"

         if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Create a unique name file
            change_filename = request.form["recipe_name"] + "_" + request.form["cuisine"] + "_" + filename

            mongo.save_file(change_filename, file)
            
            if not recipe_img == "empty":       
               fs_file = mongo.db.fs.files
               fs_chunks = mongo.db.fs.chunks
               fs_file_id = fs_file.find_one({"filename": recipe_img})


               # Remove img from DB fs.file
               fs_file.remove(
                  {"filename": recipe_img}
               )

               # Remove img from DB fs.chunks
               fs_chunks.remove(
                  {"files_id": ObjectId(fs_file_id["_id"])}
               )
            
            user.update(
            {
               "name": username,
               "recipe_cards.recipe_name": recipe_name
            },
            {
               "$set": {
                  "recipe_cards.$.img": change_filename,
                  "recipe_cards.$.recipe_name": request.form["recipe_name"].capitalize(),
                  "recipe_cards.$.cuisine": request.form["cuisine"].capitalize(),
                  "recipe_cards.$.recipe": request.form["recipe"],
                  "recipe_cards.$.cooked": int(request.form["cooked"])
               }
            })

      else:
         user.update(
            {
               "name": username,
               "recipe_cards.recipe_name": recipe_name
            },
            {
               "$set": {
                  "recipe_cards.$.recipe_name": request.form["recipe_name"].capitalize(),
                  "recipe_cards.$.cuisine": request.form["cuisine"].capitalize(),
                  "recipe_cards.$.recipe": request.form["recipe"],
                  "recipe_cards.$.cooked": int(request.form["cooked"])
               }
            }
         )

      return redirect(url_for("main_page", username=session["username"]))


@app.route("/main_page/remove_foodcard", methods=['GET', 'POST'])
def remove_cookcard(): 
   if request.method == "POST":
      user = mongo.db.users

      username = request.form["username"]
      recipe_name = request.form["recipe_name"]
      img_name = request.form["img_name"]
      current_page = int(request.form["current_page"])
      
      # Remove selected foodcard from DB
      user.update(
         {
            "name": username
         },
         {
            "$pull": {
               "recipe_cards": {"recipe_name": recipe_name},
            }
         }
      )
      
      if not img_name == "empty":       
         fs_file = mongo.db.fs.files
         fs_chunks = mongo.db.fs.chunks
         fs_file_id = fs_file.find_one({"filename": img_name})


         # Remove img from DB fs.file
         fs_file.remove(
            {"filename": img_name}
         )

         # Remove img from DB fs.chunks
         fs_chunks.remove(
            {"files_id": ObjectId(fs_file_id["_id"])}
         )

      return get_pagination(user, username, current_page)


@app.route("/main_page/cooked", methods=['GET', 'POST'])
def add_cooked(): 
   if request.method == "POST":
      user = mongo.db.users

      username = request.form["username"]
      recipe_name = request.form["recipe_name"]
      cooked = request.form["cooked"]
      current_page = int(request.form["current_page"])

      cooked_incremented = int(cooked) + 1

      user.update(
         {
            "name": username,
            "recipe_cards.recipe_name": recipe_name
         },
         {
            "$set": {
               "recipe_cards.$.cooked": cooked_incremented
            }
         })

      return get_pagination(user, username, current_page)


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('landing_page'))

if __name__ == '__main__':
   app.run(debug=True)

'''
host=os.environ.get('IP'), port=int(os.environ.get('PORT')),
'''