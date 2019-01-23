from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchemaOpts

from database.models import (Allergen, Customer, db, FoodProduct, Group, Material, Pet, Product, User, Tag,
                             TextileProduct)

ma = Marshmallow()


class BaseOptions(ModelSchemaOpts):
    """
    Basic options class to use in schemas - initially just the session.
    """
    def __init__(self, meta, *args, **kwargs):
        if not hasattr(meta, 'sql_session'):
            meta.sqla_session = db.session
        super().__init__(meta, *args, **kwargs)


class BaseModelSchema(ma.ModelSchema):
    OPTIONS_CLASS = BaseOptions

    def load(self, data, *args, **kwargs):
        """
        Allows converting keys to dictionaries {'name': 'key'} or lists/dictionaries of them
        :param data: Any, json data received at the Api endpoint.
        :return:
        """
        if isinstance(data, list):
            data = [{'name': item} for item in data]
        elif isinstance(data, str):
            data = {'name': data}
        return super().load(data, *args, **kwargs)


class PetSchema(BaseModelSchema):
    class Meta:
        model = Pet


class UserSchema(BaseModelSchema):
    pets = fields.Nested('PetSchema', many=True)

    class Meta:
        model = User


class GroupSchema(BaseModelSchema):
    class Meta:
        model = Group


class TagSchema(BaseModelSchema):
    class Meta:
        model = Tag


class MaterialSchema(ma.ModelSchema):
    class Meta:
        model = Material
        sqla_session = db.session


class AllergenSchema(BaseModelSchema):
    class Meta:
        model = Allergen


class CustomerSchema(BaseModelSchema):
    class Meta:
        model = Customer


class ProductSchema(ma.ModelSchema):
    tags = fields.Nested('TagSchema', many=True, required=True)
    materials = fields.Nested('MaterialSchema', many=True, required=True, data_key='billOfMaterials')

    class Meta:
        model = Product
        sqla_session = db.session


class FoodProductSchema(ProductSchema):
    group = fields.Nested('GroupSchema', required=True, data_key='family')
    allergens = fields.Nested('AllergenSchema', many=True, required=True)
    customer = fields.Nested('CustomerSchema', required=True)

    class Meta:
        model = FoodProduct
        sqla_session = db.session


class TextileProductSchema(ProductSchema):
    group = fields.Nested('GroupSchema', required=True, data_key='range')

    class Meta:
        model = TextileProduct
        sqla_session = db.session
