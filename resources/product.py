from http import HTTPStatus

from flask import request
from flask_restful import Resource

from config import MESSAGES, UNKNOWN_API_KEY, NO_JSON
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
    def dispatch_request(self, *args, **kwargs):
        super().dispatch_request(*args, **kwargs)
        product_type = request.headers['X-API-KEY']
        self.product_type = product_type
        # confirm correct API key used.
        if product_type not in INDUSTRY_KEYS:
            return MESSAGES[UNKNOWN_API_KEY], HTTPStatus.FORBIDDEN

    def get(self):
        schema = SCHEMAS[self.product_type][MANY]
        model = schema.Meta.model
        products = model.query.all()
        products = schema.dump(products).data
        return {f'{model.__name__}': products}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return MESSAGES[NO_JSON], HTTPStatus.BAD_REQUEST
        schema = SCHEMAS[self.product_type][SINGLE]
        model = schema.Meta.model
        product, errors = schema.load(json_data)
        if errors:
            return errors, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.add(product)
        db.session.commit()

        result = schema.dump(product).data
        return {'status': 'success', f'{model.__name__}': result}, HTTPStatus.CREATED
