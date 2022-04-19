from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username) # find a user by username
    if user and user.password == password: # compare user and password
        return user # used to generate the JWT token

# whenever they request an endpoint where they need to be authenticated, use identity
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)