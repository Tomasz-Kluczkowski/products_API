from flask import Blueprint
from flask_restful import Api

from resources.pet import PetList, PetResource
from resources.user import UserList, UserResource, UserPets

# from resources.product import ProductResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(UserList, '/users/')
api.add_resource(UserResource, '/users/<int:id>/')
api.add_resource(UserPets, '/users/<int:id>/pets/')

api.add_resource(PetList, '/pets/')
api.add_resource(PetResource, '/pets/<int:id>/')
# api.add_resource(ProductResource, '/product')
