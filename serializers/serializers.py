import marshmallow
from devtools import debug
from marshmallow_sqlalchemy import ModelSchemaOpts, ModelSchema
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

from database.models import (Allergen, Customer, db, FoodProduct, Group, Material, Pet, Product, User, Tag,
                             TextileProduct)


# class BaseOptions(ModelSchemaOpts):
#     """
#     Basic options class to use in schemas - initially adds just the session.
#     """
#     def __init__(self, meta, *args, **kwargs):
#         if not hasattr(meta, 'sql_session'):
#             meta.sqla_session = db.session
#         super().__init__(meta, *args, **kwargs)


# class BaseModelSchema(ModelSchema):
#     """
#     Adds db.session to Meta.
#     """
#     OPTIONS_CLASS = BaseOptions


# class UniqueModelSchema(BaseModelSchema):
#     """
#     Use in all schemas which should implement unique object names.
#     """
#
#     def get_instance(self, data: dict):
#         """
#         Returns an existing instance of a given object with parameters in data or None.
#         """
#         obj = self.session.query(self.opts.model).filter_by(**data).first()
#         return obj


class PetSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()

    class Meta:
        type_ = 'pets'
        self_view = 'api.petresource'
        self_view_kwargs = {'id': '<id>', '_external': True}
        self_view_many = 'api.petlist'


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    pets = Relationship(
        schema='PetSchema',
        include_resource_linkage=True,
        related_view='api.userpets',
        related_view_kwargs={'id': '<id>', '_external': True},
        many=True,
        type_='pets'
    )

    class Meta:
        type_ = 'users'
        self_view = 'api.userresource'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.userlist'
        strict = True




# class GroupSchema(UniqueModelSchema):
#     class Meta:
#         model = Group
#         exclude = ('products', )
#
#
# class TagSchema(UniqueModelSchema):
#     class Meta:
#         model = Tag
#
#
# class AllergenSchema(UniqueModelSchema):
#     class Meta:
#         model = Allergen
#
#
# class CustomerSchema(UniqueModelSchema):
#     class Meta:
#         model = Customer
#         exclude = ('food_products', )
#
#
# class MaterialSchema(BaseModelSchema):
#     class Meta:
#         model = Material
#
#
# class ProductSchema(BaseModelSchema):
#     tags = fields.Nested('TagSchema', many=True, required=True)
#     materials = fields.Nested('MaterialSchema', many=True, required=True, data_key='billOfMaterials')
#
#     class Meta:
#         model = Product
#
#
# class FoodProductSchema(ProductSchema):
#     group = fields.Nested('GroupSchema', required=True, data_key='family')
#     allergens = fields.Nested('AllergenSchema', many=True, required=True)
#     customer = fields.Nested('CustomerSchema', required=True)
#
#     class Meta:
#         model = FoodProduct
#
#
# class TextileProductSchema(ProductSchema):
#     group = fields.Nested('GroupSchema', required=True, data_key='range')
#
#     class Meta:
#         model = TextileProduct
