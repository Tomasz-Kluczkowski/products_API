from database.models import User, Pet, Toy


def test_add_user(db):
    user = User(first_name='Tom', last_name='Klucz')
    session = db.session
    session.add(user)
    session.commit()
    user_db = User.query.filter_by(first_name='Tom').first()
    assert user_db.first_name == 'Tom'
    assert user_db.last_name == 'Klucz'


def test_add_user_and_pets(db):
    pet_1 = Pet(name='Burek')
    pet_2 = Pet(name='Reksio')
    user = User(first_name='Tom', last_name='Klucz', pets=[pet_1, pet_2])
    session = db.session
    session.add(user)
    session.commit()
    user_db = User.query.filter_by(first_name='Tom').first()
    assert user_db.first_name == 'Tom'
    assert user_db.last_name == 'Klucz'
    assert user.pets == [pet_1, pet_2]


def test_delete_user_and_check_all_children_relations_deleted(db):
    toy_1 = Toy(name='Big Bone')
    toy_2 = Toy(name='Dirty Rug')
    pet_1 = Pet(name='Burek', toys=[toy_1, toy_2])
    pet_2 = Pet(name='Reksio')
    user = User(first_name='Tom', last_name='Klucz', pets=[pet_1, pet_2])
    session = db.session
    session.add(user)
    session.commit()
    user_db = User.query.filter_by(first_name='Tom').first()
    assert user_db.first_name == 'Tom'
    assert user_db.last_name == 'Klucz'
    assert user.pets == [pet_1, pet_2]

    session.delete(user_db)
    session.commit()
    assert User.query.count() == 0
    assert Pet.query.count() == 0
    assert Toy.query.count() == 0
