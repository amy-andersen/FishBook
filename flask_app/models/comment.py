from flask_app.config.mysqlconnection import connectToMySQL

class Comment:
    db_name = "fishing_schema"

    def __init__( self , data):
        self.id = data['id']
        self.comments = data['comments']
        self.trip_id = data['trip_id']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#insert a new comment to db
    @classmethod
    def save(cls, data):
        query = "INSERT INTO comments (comments, trip_id , user_id) VALUES (%(comments)s, %(trip_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

#get all the comments for a given trip
    @classmethod
    def get_one_trip_comments(cls, data):
        #display only the three latest comments
        query = "SELECT * FROM comments WHERE trip_id = %(trip_id)s ORDER BY created_at DESC LIMIT 3"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        comments = []
        for db_row in result:
            comments.append(cls(db_row))
        return comments