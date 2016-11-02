from shuttl import db

import sqlalchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.dynamic import Query

class DoNotSerializeException(Exception): pass

## Base model for all Model objects
class BaseModel(object):

    ## the ID of the object.
    id = db.Column(db.Integer, primary_key=True)

    ## tells SQLAlchemy what to call the table.
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    ## Saves the object to the data base. In case of an error, this rolls back the session and re-raises the issue.
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            pass
        except:
            db.session.rollback()
            raise
        pass

    ## Delete the object from the database
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        pass

    ## Checks to see if two objects are the equal, essentially if the IDs are equal and they are the same type
    # \param other the object to check if its equal
    # \return true if the two objects are equal, false otherwise.
    def __eq__(self, other):
        if other is None:
            return False
        return self.id == other.id and type(self) == type(other)

    ## Hashes the objects. usage: hash(object)
    # \return the hash of the ID.
    def __hash__(self):
        return hash(self.id)

    ## a property that holds all of the fields that the JSON representation will hold. By default, this will contain all
    # relationships and columns of the object.
    # \note to override this method, you can make the list yourself (eg: ["name", "id", "face"]) or you can call the base
    # method and add or remove fields from the result (eg: res = super(Class, self).__json__(); res.add("face"))
    # \return a set containing all properties to add to the serialization
    @property
    def __json__(self):
        fields = {c.name.replace("_id", "") for c in self.__table__.columns}
        for i in self.__mapper__.relationships:
            if i.key not in fields:
                fields.add(i.key)
                pass
        return fields

    ## creates an object and then saves the object.
    @classmethod
    def Create(cls, *args, **kwargs):
        inst = cls(*args, **kwargs)
        inst.save()
        return inst

    ## This tries to cast all of the possible objects into json serializable objects (eg, strings, ints, and bools)
    # this is gets called recursively to try to make every object JSON Serializable. This does most of the serialization
    # work. This is Private.
    # \param obj the object to serialize
    # \param stack a set of all BaseModel (or a subclass) objects that have been serialized
    # \param level this is to prevent the serialization from going to deep.
    # \raises DoNotSerializeException if the level = -1 or obj is in the stack
    # \return this function returns many different things. If obj is a BaseModel (or a subclass), then this will return
    # a dictionary. If obj is a list or a subclass of Query, this returns a list containing all objects in the original
    # list serialized. If obj is not a str, int, float, or bool, this returns obj casted to a string. otherwise this
    # returns obj
    def _serialize(self, obj, stack, level):
        isSubClass = issubclass(obj.__class__, BaseModel)
        if isSubClass and obj in stack or level + 1 == 0:
            raise DoNotSerializeException
        if isSubClass and obj not in stack:
            return obj.serialize(stack=stack, max_level=level-1)
        elif type(obj) not in {str, int, float, bool}:
            try:
                objIter = iter(obj)
                lst = []
                for i in objIter:
                    try:
                        lst.append(self._serialize(i, stack, level))
                        pass
                    except DoNotSerializeException:
                        continue
                    pass
                return lst
            except TypeError:
                return str(obj)
            pass
        return obj


    ## This is the public function that will get called when the object needs to be serialized.
    # \param stack this is a set of all rendered objects. This is to prevent infinite recursion (eg. An organization
    # serializes a website -> the website serializes the organization again -> the organization serializes the website
    # again . . . this continues forever). This defaults to none because of
    # http://docs.python-guide.org/en/latest/writing/gotchas/
    # \param max_level this is how many BaseModel objects you want to render. The Default is 10, for infinite use
    # float("inf")
    # \return a dictionary representing the object.
    # \note why return a dictionary over a JSON string? Its trivial to convert a dictionary to a JSON string, so I rather
    # return a dictionary because an dictionary is easier to modify than a string. You can convert the JSON string to
    # a dictionary trivially but then you have to convert it back to JSON string and you still have a dictionary. SO why
    # not just return a dictionary?

    def serialize(self, stack=None, max_level=10, *args, **kwargs):
        if stack is None:
            stack = set()
            pass
        stack.add(self)
        dictionary = {}
        for name in self.__json__:
            try:
                value = self._serialize(getattr(self, name), stack, max_level)
                pass
            except (DoNotSerializeException, AttributeError):
                continue
            dictionary[name] = value
            pass
        return dictionary
