from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()  # going to run the request through it, and match the ones defined in the parser
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'store_id',
        'price',
        type=float,
        required=True,
        help="Every item needs a store id."
    )

    # reads
    @jwt_required() # pass in JWT token to authorize
    #gets item from list and returns it
    # can just return dict if using flask restful
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    # creates
    def post(self, name):
        # if we found an item which is not None, then return message
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400 # 400=something went wrong with request
        # 400 is bad request
        # data = request.get_json()  # if req doesn't attach json payload or incorrect header, this will give an error
        # force=True, don't look at the header, silent=True - instead of giving an error, returns None

        data = Item.parser.parse_args() # parse using parser

        item = ItemModel(name, data['price'], data['store_id'])  # create JSON of the item

        try:
            item.save_to_db()
        except:  # if insert fails
            return {"message": "An error occurred inserting the item"}, 500  # 500 = internal server error

        return item.json(), 201  # status for created, means item has been created and added to database

    # deletes
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    # updates
    def put(self, name):
        data = Item.parser.parse_args() # parse the args that go through the JSON payload, and put the valid ones in data

        item = ItemModel.find_by_name(name)

        if item is None:  # not found in database
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}  # .all() returns all of the objects in the database
        # can also do a lambda function {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}