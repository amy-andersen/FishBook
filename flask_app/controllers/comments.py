from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models import comment

#post method to add a comment
@app.route('/comment', methods = ["POST"])
def add_comment():
    if "user_id" not in session: # If not logged in send to login page
        return redirect("/")
    data = {
        "comments": request.form["comments"],
        "trip_id": request.form["trip_id"],
        "user_id": session["user_id"],
    }
    comment.Comment.save(data)
    return redirect('/home')