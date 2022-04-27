from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.trip import Trip
from flask_app.models.comment import Comment


# post method to add a comment
@app.route('/comment', methods=["POST"])
def add_comment():
    print(request.form)
    if "user_id" not in session:  # If not logged in send to login page
        return redirect("/")
    data = {
        "comments": request.form["comments"],
        "trip_id": request.form["trip_id"],
        "user_id": session["user_id"],
    }
    Comment.save(data)
    return redirect('/trips')


@app.route('/new/comment/<int:trip_id>')
def comment_display(trip_id):
    if "user_id" not in session:  # If not logged in send to login page
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    this_user = User.get_one_user(data)
    trips = Trip.get_all_trips_with_comments()
    return render_template("new_comment.html", trip_id=trip_id, this_user=this_user, trips=trips)
