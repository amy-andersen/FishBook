from flask_app import app
from flask import render_template,redirect,request,session
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user

#display page for registration form
@app.route('/register')
def register():
    return render_template("register.html")

#post method for registration
@app.route('/registernewuser', methods=["POST"])
def add_new_user():
    # Validate data
    if not user.User.validate_registration(request.form):
        return redirect("/") # Send user back to login page
    # Create the new user
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form['password']),
    }
    # Save new user id in session if successful and send to login page
    session["user_id"] = user.User.save(data)
    return redirect("/")

#display page for login form
@app.route('/')
def login():
    return render_template("login.html")

#post method for login
@app.route('/login', methods=["POST"])
def userlogin():
    data = {
        "email": request.form["email"],
        "password": request.form["password"]
    }
    is_valid = user.User.validate_login(data)
    if is_valid == False: # Invalid input from form, send back to login page
        return redirect("/")
    else:
        session["user_id"] = is_valid # Set session variable = ID, go to home page
        return redirect("/trips")

#display page for user profile/ all user's trips
@app.route('/user/<int:id>')
def show_trips(id):
    if "user_id" not in session: # If not logged in send to login page
        return redirect("/")
    data = {
        "id": id,
    }
    user_data = {
        "id": session["user_id"]
    }
    user_trips = user.User.get_user_with_trips(data)
    return render_template("user_trips.html", user_trips = user_trips, user=user.User.get_one_user(user_data))

#method for logout
@app.route('/logout')
def logout():
    session.clear() # Forget user_id
    return redirect("/")