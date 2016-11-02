from .Base import BaseValidator
from shuttl import db

## A class That represents a directory
class ResellerValidator(BaseValidator):

    ##Id of the directory. Because of the way inheritance is set up in sqlalchemy, this is a foriegnKey
    id = db.Column(db.Integer, db.ForeignKey('base_validator.id'), primary_key=True)

    ## The arguments for the polymorphic behavior. SQLAlchemy link: http://docs.sqlalchemy.org/en/latest/orm/inheritance.html
    __mapper_args__ = {
        'polymorphic_identity':'reseller_validator',
    }

    ## Generates the URL for this user to go to to validate their account
    # \param reseller the reseller to validate
    def getUrl(self, reseller):
        return "{0}/validate/{1}".format(reseller.url, self.token)

