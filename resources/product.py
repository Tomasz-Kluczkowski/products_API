from http import HTTPStatus

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

    @staticmethod
    def _cleanse_data(data: dict):
        """
        Cleanse data before using it in the schemas. We need to convert simple keys or items
        in the lists / dictionaries to contain 'name' key and value.
        """
        for key, value in data.items():
            if isinstance(value, str) and key != 'name':
                data[key] = {'name': value}
            elif isinstance(value, list):
                data[key] = [{'name': item} for item in value]
            elif isinstance(value, dict):
                data[key] = [{'name': key, **params} for key, params in value.items()]

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
        self._cleanse_data(json_data)
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
