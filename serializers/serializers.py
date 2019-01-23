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
    def __init__(self, meta):
        if not hasattr(meta, 'sql_session'):
            meta.sqla_session = db.session
        super().__init__(meta)


class BaseModelSchema(ma.ModelSchema):
    OPTIONS_CLASS = BaseOptions


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


class MaterialSchema(BaseModelSchema):
    class Meta:
        model = Material


class AllergenSchema(BaseModelSchema):
    class Meta:
        model = Allergen


class CustomerSchema(BaseModelSchema):
    class Meta:
        model = Customer


class ProductSchema(BaseModelSchema):
    group = fields.Nested('Group', required=True)
    tags = fields.Nested('Tag', many=True, required=True)
    materials = fields.Nested('Material', many=True, required=True)

    class Meta:
        model = Product


class FoodProductSchema(ProductSchema):
    allergens = fields.Nested('Allergen', many=True, required=True)
    customer = fields.Nested('Customer', required=True)

    class Meta:
        model = FoodProduct


class TextileProductSchema(ProductSchema):
    class Meta:
        model = TextileProduct
