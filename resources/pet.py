from devtools import debug
from flask import request, make_response, jsonify
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from database.models import db, Pet
from serializers.serializers import PetSchema

pet_schema = PetSchema()
pets_schema = PetSchema(many=True)


class PetList(Resource):
    """
    Provide CRUD operations for user objects.
    """
    def get(self):
        pets = Pet.query.all()
        pets = pets_schema.dump(pets)
        return pets, 200

    def post(self):
        json_data = request.get_json(force=True)
        debug(json_data)
        if not json_data:
            return {'message': 'No input data'}, 400
        try:
            result = pet_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        debug(result)
        pet = Pet(**result)
        db.session.add(pet)
        db.session.commit()

        result = pet_schema.dump(pet)
        return {'status': 'success', 'pet': result}, 201


class PetResource(Resource):
    """
    Provide detail view and operations.
    """
    def get(self, id):
        pet_query = Pet.query.get_or_404(id)
        result = pet_schema.dump(pet_query)
        return result

    def delete(self, id):
        pet = Pet.query.get_or_404(id)
        try:
            db.session.delete(pet)
            db.session.commit()
            response = make_response()
            response.status_code = 204
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp
