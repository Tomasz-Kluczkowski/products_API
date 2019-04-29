import inspect
from typing import List, Optional, Type, Dict

from devtools import debug
from marshmallow import post_load, fields
from marshmallow_annotations import AnnotationSchema
from marshmallow_sqlalchemy import ModelSchema
from database.models import Pet as PetPM, User as UserPM, Toy as ToyPM


DEFAULT_ID = 'DEFAULT_ID'

def make_object_from_dict(cls: Type, data: Dict):
    """
    Parses the output of `marshmallow.load` into an object of the given cls
    Parameters
    ----------
    cls
        The type of the object to make
    data
        The data to be parsed in. This is the result of the `.load` method on a marshmallow schema

    Notes
    -----
    If the object we're creating requires an id but no id is provided, one will be generated using `generate_id`

    """
    if not cls:
        raise ValueError('`_cls` must be specified')
    if not isinstance(cls, type):
        raise ValueError('`_cls` must be a class definition')

    sig = inspect.signature(cls.__init__)
    if 'id_' in sig.parameters and 'id_' not in data:
        data['id_'] = data.get('id', DEFAULT_ID)
    if 'id' not in sig.parameters and 'id' in data:
        del data['id']
    if 'id' in sig.parameters and 'id' not in data:
        data['id'] = DEFAULT_ID

    data = {k: v for k, v in data.items() if k in sig.parameters}

    return cls(**data)


class SchemaPostLoadMixin:
    """ Mixin which adds a post_load method, taking the output dict of a Marshmallow schema .load() as the arguments
    of _cls init. Use this to load json into a domain model."""
    # _cls = None
    #
    # def __init__(self, cls=None, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if cls is not None:
    #         self._cls = cls

    @post_load
    def make_object(self, data):
        return make_object_from_dict(self.opts.target, data)


class Pet:
    id: str
    name: str

    def __init__(self, id_: str, name: str):
        self.id = id_
        self.name = name


class User:
    id: str
    first_name: str
    last_name: str
    pets: Optional[List[Pet]]

    def __init__(self, id_: str, first_name: str, last_name: str, pets: List[Pet] = None):
        self.id = id_
        self.first_name = first_name
        self.last_name = last_name
        self.pets = pets


class PetSchema(AnnotationSchema):
    class Meta:
        target = Pet
        register_as_scheme = True


class UserSchema(AnnotationSchema):
    class Meta:
        target = User
        register_as_scheme = True


class PetModelSchema(ModelSchema):
    class Meta:
        model = PetPM

    toys = fields.Nested('ToyModelSchema', many=True)


class ToyModelSchema(ModelSchema):
    class Meta:
        model = ToyPM


class UserModelSchema(ModelSchema):
    class Meta:
        model = UserPM

    pets = fields.Nested('PetModelSchema', many=True)

toy_pm = ToyPM(id=1, name='toy_1', pet_id=1)
pet_pm = PetPM(id=1, name='Burek', user_id=1, toys=[toy_pm])
user_pm = UserPM(id=1, first_name='Tomek', last_name='Kluczkowski', pets=[pet_pm])

# pet1 = Pet(id_='pet_id_1', name='Reksio')
# pet2 = Pet(id_='pet_id_2', name='Burek')
# user = User(id_='tomek_id', first_name='Tomek', last_name='Kluczkowski', pets=[pet1, pet2])

# schema = UserSchema()
#
# debug(schema.dump(user).data)
user_schema = UserModelSchema()

debug(user_schema.dump(user_pm).data)


class PetSchemaDomain(PetSchema, SchemaPostLoadMixin):
    pass

