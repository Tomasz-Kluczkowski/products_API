from http import HTTPStatus

from devtools import debug
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from config import MESSAGES, UNKNOWN_API_KEY, NO_JSON, DUPLICATE_PRODUCT
from database.models import db
from industries.industries_config import INDUSTRY_KEYS, FOOD, TEXTILES
from serializers.serializers import FoodProductSchema, TextileProductSchema

SINGLE = 'single'
MANY = 'many'

food_product_schema = FoodProductSchema()
food_products_schema = FoodProductSchema(many=True)

textile_product_schema = TextileProductSchema()
textile_products_schema = TextileProductSchema(many=True)

SCHEMAS = {
    FOOD: {
        SINGLE: food_product_schema,
        MANY: food_products_schema
    },
    TEXTILES: {
        SINGLE: textile_product_schema,
        MANY: textile_products_schema
    }
}


class ProductResource(Resource):
    """
    Provide CRUD operations for product objects.
    """
    def __init__(self):
        super().__init__()
        self.product_type = None

    def dispatch_request(self, *args, **kwargs):
        product_type = request.headers.get('X-API-KEY')
        self.product_type = product_type
        # confirm correct API key used.
        if product_type not in INDUSTRY_KEYS:
            return MESSAGES[UNKNOWN_API_KEY], HTTPStatus.FORBIDDEN
        return super().dispatch_request(*args, **kwargs)

    def get(self):
        schema = SCHEMAS[self.product_type][MANY]
        model = schema.Meta.model
        products = model.query.all()
        products = schema.dump(products)
        return {f'{model.__name__}': products}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return MESSAGES[NO_JSON], HTTPStatus.BAD_REQUEST
        schema = SCHEMAS[self.product_type][SINGLE]
        model = schema.Meta.model
        try:
            product = schema.load(json_data)
        except ValidationError as err:
            return err.messages, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.add(product)
        try:
            db.session.commit()
        except IntegrityError:
            return MESSAGES[DUPLICATE_PRODUCT], HTTPStatus.UNPROCESSABLE_ENTITY

        result = schema.dump(product)
        return {'status': 'success', f'{model.__name__}': result}, HTTPStatus.CREATED
