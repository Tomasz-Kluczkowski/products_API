from flask_marshmallow import Marshmallow
from marshmallow import fields


from database.models import db, Pet, User

ma = Marshmallow()


class PetSchema(ma.ModelSchema):
    class Meta:
        model = Pet
        sqla_session = db.session


class UserSchema(ma.ModelSchema):
    pets = fields.Nested('PetSchema', many=True)

    class Meta:
        model = User
        sqla_session = db.session
