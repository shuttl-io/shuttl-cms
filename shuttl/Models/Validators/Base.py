import datetime
import random
from sqlalchemy.exc import IntegrityError
import string

from shuttl import db, app
from shuttl.database import BaseModel

class InvalidValidator(Exception): pass

## An Abstract Base Class to represent objects in a directory structure
class BaseValidator(db.Model, BaseModel):
    ## Id of the file object
    id = db.Column(db.Integer, primary_key=True)

    ## the id of the user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    ##The unique token of the validator
    token = db.Column(db.String, unique=True, index=True)

    ## The time the validator was issued, if to old, validator is invalid
    issued = db.Column(db.DateTime, nullable=False)

    type = db.Column(db.String(50))

    ## The arguments for the polymorphic behavior. SQLAlchemy link: http://docs.sqlalchemy.org/en/latest/orm/inheritance.html
    __mapper_args__ = {
        'polymorphic_identity':'base_validator',
        'polymorphic_on': type
    }

    ## Generates a random token of len size
    # \param size the number of chars (Defaults to 64)
    # \param chars the chars allowed to appear in the token. (defaults to all letters and numbers 0-9)
    # \returns a string of len size
    def generateToken(self, size=64, chars=string.ascii_letters+string.digits):
        return "".join((random.choice(chars) for _ in range(size)))

    ## Generates the URL for this user to go to to validate their account
    # \raises not implemented error
    def getUrl(self, *args, **kwargs):
        raise NotImplementedError

    ## Creates the Validator
    # \param user the user that is being validated
    # \returns the validator
    @classmethod
    def Create(cls, user, *args, **kwargs):
        def _create():
            validator = cls(user_id=user.id)
            validator.token = validator.generateToken()
            validator.issued = datetime.datetime.now()
            validator.save()
            return validator
        try:
            validator = _create()
        except IntegrityError:
            # A user must already have a validator, delete it and then create a new one.
            validator = cls.query.filter(cls.user_id==user.id).first()
            validator.delete()
            validator = _create()
            pass
        return validator

    ## Make a polymorphic Query, this will automatically cast objects to their inherited classes
    # \param cls_or_all defualts to ("*") this is the classes that we should cast to
    @classmethod
    def polyQuery(cls, cls_or_all=("*")):
        return cls.query.with_polymorphic(*cls_or_all)

    ## Indicates if a validator is expired. Also deletes the validator if expired.
    # \return true if validator is expired false otherwise
    def isExpired(self):
        expired = datetime.datetime.now() - self.issued > app.config["VALID_EXP"]
        if expired:
            self.delete()
            pass
        return expired

    ## validates a token and checks to see if the user "owns" this validator. If yes, set user.isActive to true
    # \param token the validation token
    # \param user the user who wants to be validated.
    @classmethod
    def Validate(cls, token, user):
        validator = cls.polyQuery().filter(BaseValidator.token==token).first()
        if validator is None:
            raise InvalidValidator
        if validator.isExpired() or user.id != validator.user_id:
            raise InvalidValidator
        user.isActive = True
        user.sendHelloEmail()
        user.save()
        pass
