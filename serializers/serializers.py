from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchemaOpts

from database.models import (Allergen, Customer, db, FoodProduct, Group, Material, Pet, Product, User, Tag,
                             TextileProduct)

ma = Marshmallow()


class BaseOptions(ModelSchemaOpts):
    """
    Basic options class to use in schemas - initially adds just the session.
    """
    def __init__(self, meta, *args, **kwargs):
        if not hasattr(meta, 'sql_session'):
            meta.sqla_session = db.session
        super().__init__(meta, *args, **kwargs)


class BaseModelSchema(ma.ModelSchema):
    """
    Adds db.session to Meta.
    """
    OPTIONS_CLASS = BaseOptions


class LoadModelSchema(BaseModelSchema):

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


class GroupSchema(LoadModelSchema):
    class Meta:
        model = Group


class TagSchema(LoadModelSchema):
    class Meta:
        model = Tag


class AllergenSchema(LoadModelSchema):
    class Meta:
        model = Allergen


class CustomerSchema(LoadModelSchema):
    class Meta:
        model = Customer


class MaterialSchema(BaseModelSchema):
    class Meta:
        model = Material


class ProductSchema(BaseModelSchema):
    tags = fields.Nested('TagSchema', many=True, required=True)
    materials = fields.Nested('MaterialSchema', many=True, required=True, data_key='billOfMaterials')

    class Meta:
        model = Product


class FoodProductSchema(ProductSchema):
    group = fields.Nested('GroupSchema', required=True, data_key='family')
    allergens = fields.Nested('AllergenSchema', many=True, required=True)
    customer = fields.Nested('CustomerSchema', required=True)

    class Meta:
        model = FoodProduct


class TextileProductSchema(ProductSchema):
    group = fields.Nested('GroupSchema', required=True, data_key='range')

    class Meta:
        model = TextileProduct
