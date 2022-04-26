# from flask_app.models.trip import trip
from flask_app.models.user import User
from flask_app.models.trip import Trip
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# display page for registration form


@app.route('/')
def index():
    return render_template("register.html")

# post method for registration


@app.route('/register', methods=['POST'])
def register():

    if not User.validate_registration(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/login/page')


@app.route('/login/page')
def login_page():
    return render_template('login.html')

# post method for login


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email", "login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/login')
    session['user_id'] = user.id
    return redirect('/trips')

# display page for user profile/ all user's trips


@app.route('/user/<int:id>')
def show_trips(id):
    if "user_id" not in session:  # If not logged in send to login page
        return redirect("/")
    data = {
        "id": id,
    }
    user_data = {
        "id": session["user_id"]
    }
    return render_template("user_trips.html", user=User.get_user_with_trips(user_data))


@app.route('/trips')
def trips():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user_trips = User.get_user_with_trips(data)
    return render_template("all_trips.html", user_trips=user_trips, trips=Trip.get_all_trips_with_comments())

# method for logout


@app.route('/logout')
def logout():
    session.clear()  # Forget user_id
    return redirect("/")
