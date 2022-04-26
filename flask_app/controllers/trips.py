from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.trip import Trip
from flask_app.models.user import User

# display home page


@app.route('/trips')
def home():
    if "user_id" not in session:  # If not logged in send to login page
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    this_user = User.get_one_user(data)
    trips = Trip.get_all_trips_with_comments()
    return render_template("all_trips.html", this_user=this_user, trips=trips)

# display add trip page


@app.route('/new')
def add_trip():
    if "user_id" not in session:  # If not logged in send to login page
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("new_trip.html", this_user=User.get_one_user(data))

# Post method to add a trip


@app.route('/add_trip', methods=["POST"])
def add():
    if "user_id" not in session:  # If not logged in send to login page
        return redirect("/logout")
    # Validate data
    if not Trip.validate_trip(request.form):
        return redirect("/home")  # Send user back home
    data = {
        "species": request.form["species"],
        "bait": request.form["bait"],
        "water": request.form["water"],
        "date_of_trip": request.form["date_of_trip"],
        "quantity": request.form["quantity"],
        "user_id": session["user_id"]
    }
    Trip.save(data)
    return redirect('/trips')

# display edit trip page


@app.route('/edit/<int:id>')
def edit_trip(id):
    if "user_id" not in session:  # If not logged in send to login page
        return redirect("/")
    data = {
        "id": id
    }
    user_data = {
        "id": session["user_id"]
    }
    return render_template("edit_trip.html", trip=Trip.get_one_trip(data), user=User.get_one_user(user_data))

# Post method to edit a trip


@app.route('/edit/trip/<int:id>', methods=["POST"])
def edit(id):
    if "user_id" not in session:  # If not logged in send to login page
        return redirect('/')
    # Validate data
    if not Trip.validate_trip(request.form):
        return redirect(f'/edit/trip/{id}')  # Send user back to edit trip
    data = {
        "species": request.form["species"],
        "bait": request.form["bait"],
        "water": request.form["water"],
        "date_of_trip": request.form["date_of_trip"],
        "quantity": request.form["quantity"],
        "user_id": session["user_id"],
        "id": id
    }
    Trip.update(data)
    return redirect(f'/user/{session["user_id"]}')

# method to delete a trip


@app.route('/delete/trip/<int:id>')
def destroy_trip(id):
    if "user_id" not in session:  # If not logged in send to login page
        return redirect("/")
    data = {
        "id": id
    }
    Trip.destroy(data)
    return redirect(f'/user/{session["user_id"]}')
