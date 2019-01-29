from database.models import FoodProduct, TextileProduct
from serializers.serializers import FoodProductSchema, TextileProductSchema
from tests.product_data import food_product_data, textile_product_data


class TestCommonAPI:

    def test_db_empty(self, db):
        session = db.session
        assert session.query(FoodProduct).count() == 0


class TestFoodAPI:

    def test_add_food_product(self, client, db):
        session = db.session

        client.post(
            '/api/product', json=food_product_data[0], content_type='application/json', headers={'x_api_key': 'food'}
        )
        assert session.query(FoodProduct).count() == 1
        food_product = session.query(FoodProduct).first()
        food_product_schema = FoodProductSchema()
        assert food_product_schema.dump(food_product) == {
            'billOfMaterials': [
                {
                    'units': 'tablespoons',
                    'name': 'paprika',
                    'quantity': 100.0,
                    'id': 1,
                },
                {
                    'units': 'kg',
                    'name': 'pork mince',
                    'quantity': 10.0,
                    'id': 2,
                },
            ],
            'allergens': [
                {
                    'name': 'cereals',
                    'id': 1,
                },
            ],
            'tags': [
                {
                    'name': 'spanish',
                    'id': 2,
                },
                {
                    'name': 'spicy',
                    'id': 1,
                },
            ],
            'customer': {
                'name': 'Deans Butchers',
                'id': 1,
            },
            'name': 'Chorizo',
            'id': 1,
            'family': {
                'name': 'sausage',
                'id': 1,
            },
            'type': 'food_product',
        }


class TestTextileAPI:

    def test_add_textile_product(self, client, db):
        session = db.session

        client.post(
            '/api/product', json=textile_product_data[0], content_type='application/json', headers={'x_api_key': 'textiles'}
        )
        assert session.query(TextileProduct).count() == 1
        textile_product = session.query(TextileProduct).first()
        textile_product_schema = TextileProductSchema()
        assert textile_product_schema.dump(textile_product) == {
            'billOfMaterials': [
                {
                    'units': 'metres',
                    'id': 1,
                    'name': 'Maroon wool',
                    'quantity': 100.0,
                },
                {
                    'units': 'square metres',
                    'id': 2,
                    'name': 'Silk lining',
                    'quantity': 10.0,
                },
            ],
            'id': 1,
            'colour': 'Maroon',
            'range': {
                'name': 'Grandad Chic',
                'id': 1,
            },
            'type': 'textile_product',
            'name': 'Tweed Jacket',
            'tags': [
                {
                    'name': 'mens',
                    'id': 1,
                },
                {
                    'name': 'smart',
                    'id': 2,
                },
                {
                    'name': 'suits',
                    'id': 3,
                },
            ],
        }
