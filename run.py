import os
from flask import Flask, render_template, url_for, session, request, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask import send_from_directory


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
                     "img" : "empty"
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
                  "recipe_name" : request.form["recipe_name"],
                  "cuisine": request.form["cuisine"],
                  "recipe" : request.form["recipe"],
                  "cooked" : 0,
                  "img" : change_filename
                  }
               }
            })
      else:
         users.update( {"name": username},
               {
                  "$push": {"recipe_cards": {
                     "recipe_name" : request.form["recipe_name"],
                     "cuisine": request.form["cuisine"],
                     "recipe" : request.form["recipe"],
                     "cooked" : 0,
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

   return render_template("edit_cookcard.html", cookcard=cookcard["recipe_cards"][0])

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
                  "recipe_cards.$.recipe_name": request.form["recipe_name"],
                  "recipe_cards.$.cuisine": request.form["cuisine"],
                  "recipe_cards.$.recipe": request.form["recipe"]
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
                  "recipe_cards.$.recipe_name": request.form["recipe_name"],
                  "recipe_cards.$.cuisine": request.form["cuisine"],
                  "recipe_cards.$.recipe": request.form["recipe"]
               }
            }
         )

      return redirect(url_for("main_page", username=session["username"]))


@app.route("/main_page/<username>/remove_foodcard/<recipe_name>/<img_name>", methods=['GET', 'POST'])
def remove_cookcard(username, recipe_name, img_name): 
   if request.method == "POST":
      user = mongo.db.users
      print("---------PRINT 111111 ---------")
      print(img_name)
      
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

      return redirect(url_for("main_page", username=session["username"]))



if __name__ == '__main__':
   app.run(debug=True)

'''
host=os.environ.get('IP'), port=int(os.environ.get('PORT')),
'''