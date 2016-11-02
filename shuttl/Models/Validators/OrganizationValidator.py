from flask import redirect, url_for
from .Base import BaseValidator
from shuttl import db
from shuttl import app


class OrganizationValidator(BaseValidator):

    ##Id of the directory. Because of the way inheritance is set up in sqlalchemy, this is a foriegnKey
    id = db.Column(db.Integer, db.ForeignKey('base_validator.id'), primary_key=True)

    ## The arguments for the polymorphic behavior. SQLAlchemy link: http://docs.sqlalchemy.org/en/latest/orm/inheritance.html
    __mapper_args__ = {
        'polymorphic_identity': 'organization_validator',
    }

    ## Generates the URL for this user to go to to validate their account
    # \param organization_name name of the organization to validate
    # \return url the url for validating a user
    def getUrl(self, organization_name):
        if organization_name is not None:
            url = "http://{0}.{1}{2}".format(organization_name, app.config["SERVER_NAME"], \
                                       url_for("shuttlOrgs.validate", organization=organization_name, token=self.token))
            return url
        pass
