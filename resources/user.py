from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError

from database.models import db, User
from serializers.serializers import UserSchema
from tasks.tasks import print_hello

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserResource(Resource):
    """
    Provide CRUD operations for user objects.
    """
    def get(self):
        users = User.query.all()
        users = users_schema.dump(users)
        return {"users": users}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data'}, 400
        try:
            user = user_schema.load(json_data).data
        except ValidationError as err:
            return err.messages, 422

        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user)
        return {'status': 'success', 'user': result}, 201
