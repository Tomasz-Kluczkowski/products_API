from database.models import FoodProduct
from tests.product_data import food_product_data


class TestFoodAPI:

    def test_db_empty(self, db):
        session = db.session
        assert session.query(FoodProduct).count() == 0

    def test_add_food_product(self, client, db):
        session = db.session

        client.post(
            '/api/product', json=food_product_data[0], content_type='application/json', headers={'x_api_key': 'food'}
        )
        assert session.query(FoodProduct).count() == 1
        food_product =  session.query(FoodProduct).first()
        assert food_product.name == 'Chorizo'


