from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    Test model to check serializing using marshmallow etc.
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    pets = db.relationship('Pet', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User(first_name={self.first_name}, last_name={self.last_name}, pets={self.pets})>'


class Pet(db.Model):
    """
    Test relationship - check nested saving
    """
    __tablename__ = 'pet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    toys = db.relationship('Toy', backref='pet', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Pet(name={self.name})>'


class Toy(db.Model):
    """
    Test relationship - check nested saving
    """
    __tablename__ = 'toy'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))

    def __repr__(self):
        return f'<Toy(name={self.name})>'


class NameBase:
    """
    Base class for all models requiring a unique name and id fields.
    """
    name = db.Column(db.String(50), unique=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True)


class Group(db.Model, NameBase):
    """
    Group model for products (i.e: family, range etc.) - more specific classification than Type.
    """
    __tablename__ = 'group'


class Tag(db.Model, NameBase):
    """
    Tag model for products.
    """
    __tablename__ = 'tag'


class Material(db.Model, NameBase):
    """
    Model of material of a product. (i. e. sugar, grams, 20)
    """
    __tablename__ = 'material'
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.FLOAT, nullable=False)
    units = db.Column(db.String(50))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


class Allergen(db.Model, NameBase):
    """
    Model for an allergen in food product.
    """
    __tablename__ = 'allergen'


class Customer(db.Model, NameBase):
    """
    Model for customer.
    """
    __tablename__ = 'customer'


product_tag = db.Table(
    'product_tag',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class Product(db.Model, NameBase):
    """
    Base product model to be extended by specific product types.
    """
    __tablename__ = 'product'
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('Group', backref='products', lazy='joined')
    tags = db.relationship('Tag', secondary=product_tag, lazy='joined')
    materials = db.relationship('Material', lazy='joined')
    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'product',
        'polymorphic_on': type
    }


product_allergens = db.Table(
    'product_allergen',
    db.Column('food_product_id', db.Integer, db.ForeignKey('food_product.id')),
    db.Column('allergen_id', db.Integer, db.ForeignKey('allergen.id'))
)


class FoodProduct(Product):
    """
    Food product model class.
    """
    __tablename__ = 'food_product'
    id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    allergens = db.relationship('Allergen', secondary=product_allergens, lazy='joined')
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship('Customer', backref='food_products', lazy='joined')
    __mapper_args__ = {
        'polymorphic_identity': 'food_product'
    }


class TextileProduct(Product):
    """
    Textile product model class.
    """
    __tablename__ = 'textiles_product'
    id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    colour = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'textile_product'
    }
