from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# having api
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # saying the sqlalchm database is going to live in root folder, doesn't have to be sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # turning it off bc SQLALCHEMY has a tracker
app.secret_key = 'jose' # secret and secure
api = Api(app)

@app.before_first_request  # Flask decorator that's going to affect the method below it, going to run the mehtod before the first request
def create_tables():  # don't need create_tables.py anymore
    db.create_all()

jwt = JWT(app, authenticate, identity) # JWT creates new endpoint: /auth

# represents database
# with in-memory databases, everytime you start the app, memory gets cleared
# items = []

# defining resource



# add resource and determine how it's going to be accessed
# similar to @app.route('/student/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

# whenever we run app.py, python assigns the file "main" name
# if not main means we imported it from elsewhere, wont run
if __name__ == '__main__':
    from db import db  # importing here bc of circular imports
    db.init_app(app)
    app.run(port=5000, debug=True)  # when you get an error page, gives nice HTML page
