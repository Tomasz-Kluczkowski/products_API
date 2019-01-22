from flask import request
from flask_restful import Resource
from database.models import db, User
from serializers.serializers import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserResource(Resource):
    """
    Provide CRUD operations for user objects.
    """
    def get(self):
        users = User.query.all()
        users = users_schema.dump(users).data
        return {"users": users}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data'}, 400

        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422

        user = User(first_name=data['first_name'], last_name=data['last_name'])

        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user).data
        return {'status': 'success', 'user': result}, 201
