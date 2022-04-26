from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash  # for flash messages
from flask_app.models.comment import Comment


class Trip:
    db_name = "fishing_schema"

    def __init__(self, data):
        self.id = data['id']
        self.species = data['species']
        self.bait = data['bait']
        self.water = data['water']
        self.date_of_trip = data['date_of_trip']
        self.quantity = data['quantity']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comments = []

# insert a new trip to db
    @classmethod
    def save(cls, data):
        query = "INSERT INTO trips (species, bait, water, date_of_trip, quantity, user_id) VALUES (%(species)s, %(bait)s, %(water)s, %(date_of_trip)s, %(quantity)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

# edit a trip
    @classmethod
    def update(cls, data):
        query = "UPDATE trips SET species=%(species)s,bait=%(bait)s,water=%(water)s, date_of_trip=%(date_of_trip)s, quantity=%(quantity)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

# delete a trip from db
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM trips WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

# get all trips with all comments
    @classmethod
    def get_all_trips_with_comments(cls):
        query = "SELECT * FROM trips;"
        results = connectToMySQL(cls.db_name).query_db(query)
        trips = []
        for db_row in results:
            trip = cls(db_row)
            trip.comments = Comment.get_one_trip_comments(
                {"trip_id": db_row["id"]})
            trips.append(trip)
        return trips

# get one trip from db
    @classmethod
    def get_one_trip(cls, data):
        query = "SELECT * FROM trips WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])

# validate trip - all fields present
    @staticmethod
    def validate_trip(data):
        is_valid = True
        if data["species"] == "":  # must be filled out
            is_valid = False
            flash("Please enter a species.", "trip")
        if data["bait"] == "":  # must be filled out
            is_valid = False
            flash("Please enter bait used.", "trip")
        if data["water"] == "":  # must be filled out
            is_valid = False
            flash("Please select a type of water.", "trip")
        if data["date_of_trip"] == "":  # must be filled out
            is_valid = False
            flash("Please enter trip date.", "trip")
        if data["quantity"] == "":  # must be filled out
            is_valid = False
            flash("Please enter a quantity.", "trip")
        return is_valid  # Return true if valid, false if not
