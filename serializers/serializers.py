from flask_marshmallow import Marshmallow

from database.models import User

ma = Marshmallow()


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
