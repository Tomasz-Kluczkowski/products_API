from devtools import debug
from flask import request, make_response, jsonify
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from database.models import db, User
from serializers.serializers import UserSchema, PetSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserList(Resource):
    """
    Provide CRUD operations for user objects.
    """
    def get(self):
        users = User.query.all()
        users = users_schema.dump(users)
        return users, 200

    def post(self):
        json_data = request.get_json(force=True)
        debug(json_data)
        if not json_data:
            return {'message': 'No input data'}, 400
        try:
            result = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        debug(result)
        user = User(**result)
        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user)
        return {'status': 'success', 'user': result}, 201


class UserResource(Resource):
    """
    Provide detail view and operations.
    """
    def get(self, id):
        user_query = User.query.get_or_404(id)
        result = user_schema.dump(user_query)
        return result

    def delete(self, id):
        user = User.query.get_or_404(id)
        try:
            db.session.delete(user)
            db.session.commit()
            response = make_response()
            response.status_code = 204
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp


class UserPets(Resource):
    """
    Fetches pets per user.
    """
    def get(self, id):
        pets = User.query.get_or_404(id).pets
        result = PetSchema(many=True).dump(pets)
        return result
