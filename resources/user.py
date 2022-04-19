import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource): # create endpoint in app.py too (line 6, 79)
    #create request parser that accepts username and password
    #parse the JSON data coming in POST request --> call data
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self):
        # parse the arguments using UserRegister parser which is going to expect a username and password
        data = UserRegister.parser.parse_args()  # got data from JSON payload

        # make sure username doesn't exist already, put after parse line above
        if UserModel.find_by_username(data['username']): # if the username doesn't return None, that mean it already exists
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)  # bc of parser
        user.save_to_db()

        return {"message": "User created successfully."}, 201
