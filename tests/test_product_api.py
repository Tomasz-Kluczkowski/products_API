import json


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
        assert food_product_schema.dump(food_product).data == {
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

    def test_get_food_products(self, client, db):
        client.post(
            '/api/product', json=food_product_data[0], content_type='application/json', headers={'x_api_key': 'food'}
        )
        client.post(
            '/api/product', json=food_product_data[1], content_type='application/json', headers={'x_api_key': 'food'}
        )
        response = client.get('/api/product', content_type='application/json', headers={'x_api_key': 'food'})
        assert json.loads(response.data) == {
            'FoodProduct': [
                {
                    'id': 1,
                    'customer': {
                        'id': 1,
                        'name': 'Deans Butchers',
                    },
                    'allergens': [
                        {
                            'id': 1,
                            'name': 'cereals',
                        },
                    ],
                    'tags': [
                        {
                            'id': 2,
                            'name': 'spanish',
                        },
                        {
                            'id': 1,
                            'name': 'spicy',
                        },
                    ],
                    'type': 'food_product',
                    'name': 'Chorizo',
                    'billOfMaterials': [
                        {
                            'units': 'tablespoons',
                            'id': 1,
                            'quantity': 100.0,
                            'name': 'paprika',
                        },
                        {
                            'units': 'kg',
                            'id': 2,
                            'quantity': 10.0,
                            'name': 'pork mince',
                        },
                    ],
                    'family': {
                        'id': 1,
                        'name': 'sausage',
                    },
                },
                {
                    'id': 2,
                    'customer': {
                        'id': 2,
                        'name': 'Sainsburys',
                    },
                    'allergens': [
                        {
                            'id': 1,
                            'name': 'cereals',
                        },
                        {
                            'id': 2,
                            'name': 'eggs',
                        },
                        {
                            'id': 3,
                            'name': 'sesame',
                        },
                    ],
                    'tags': [
                        {
                            'id': 3,
                            'name': 'BBQ',
                        },
                    ],
                    'type': 'food_product',
                    'name': 'Mighty Hamburgers',
                    'billOfMaterials': [
                        {
                            'units': 'cups',
                            'id': 3,
                            'quantity': 12.0,
                            'name': 'breadcrumbs',
                        },
                        {
                            'units': 'kg',
                            'id': 4,
                            'quantity': 56.3,
                            'name': 'minced beef',
                        },
                        {
                            'units': 'kg',
                            'id': 5,
                            'quantity': 15.0,
                            'name': 'onions',
                        },
                    ],
                    'family': {
                        'id': 2,
                        'name': 'burgers',
                    },
                },
            ],
        }


class TestTextileAPI:

    def test_add_textile_product(self, client, db):
        session = db.session

        client.post(
            '/api/product',
            json=textile_product_data[0],
            content_type='application/json',
            headers={'x_api_key': 'textiles'}
        )
        assert session.query(TextileProduct).count() == 1
        textile_product = session.query(TextileProduct).first()
        textile_product_schema = TextileProductSchema()
        assert textile_product_schema.dump(textile_product).data == {
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

    def test_get_textile_products(self, client, db):
        client.post(
            '/api/product',
            json=textile_product_data[0],
            content_type='application/json',
            headers={'x_api_key': 'textiles'}
        )
        client.post(
            '/api/product',
            json=textile_product_data[1],
            content_type='application/json',
            headers={'x_api_key': 'textiles'}
        )
        response = client.get('/api/product', content_type='application/json', headers={'x_api_key': 'textiles'})
        assert json.loads(response.data) == {
            'TextileProduct': [
                {
                    'name': 'Tweed Jacket',
                    'id': 1,
                    'billOfMaterials': [
                        {
                            'quantity': 100.0,
                            'name': 'Maroon wool',
                            'id': 1,
                            'units': 'metres',
                        },
                        {
                            'quantity': 10.0,
                            'name': 'Silk lining',
                            'id': 2,
                            'units': 'square metres',
                        },
                    ],
                    'colour': 'Maroon',
                    'type': 'textile_product',
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
                    'range': {
                        'name': 'Grandad Chic',
                        'id': 1,
                    },
                },
                {
                    'name': 'Plain T',
                    'id': 2,
                    'billOfMaterials': [
                        {
                            'quantity': 0.5,
                            'name': 'Cotton',
                            'id': 3,
                            'units': 'kilograms',
                        },
                        {
                            'quantity': 1.0,
                            'name': 'Print',
                            'id': 4,
                            'units': None,
                        },
                        {
                            'quantity': 23.0,
                            'name': 'Thread',
                            'id': 5,
                            'units': 'metres',
                        },
                        {
                            'quantity': 0.4,
                            'name': 'Water',
                            'id': 6,
                            'units': 'litres',
                        },
                    ],
                    'colour': 'Ocean Blue',
                    'type': 'textile_product',
                    'tags': [
                        {
                            'name': 'casual',
                            'id': 4,
                        },
                        {
                            'name': 'mens',
                            'id': 1,
                        },
                    ],
                    'range': {
                        'name': 'Normal',
                        'id': 2,
                    },
                },
            ],
        }
