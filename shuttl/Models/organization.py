from flask import url_for

from shuttl import app
from shuttl.database import BaseModel, db
from sqlalchemy.exc import IntegrityError
from shuttl.Models.User import User
from shuttl.Models.Website import Website


## An exception that is raised when the Organization doesn't exsit
class OrganizationDoesNotExistException(Exception): pass

## An exception that is raised when the Organization already exists
class OrganizationExists(Exception): pass


## Class to model an organization. The organization is a central component of Shuttl. This tracks Websites and Users
#
class Organization(BaseModel, db.Model):
    name = db.Column(db.String, index=True, unique=True) ##< the name of the organization ##string

    ## The many to many representation of the users. List
    users = db.relationship("User", back_populates="organization")

    ##List of websites for the organization.
    websites = db.relationship("Website", backref='organization', lazy='dynamic')

    ## the reseller that this organization
    reseller_id = db.Column(db.Integer, db.ForeignKey('reseller.id'), nullable=False)

    reseller = db.relationship("Reseller", foreign_keys=[reseller_id], back_populates="organizations")

    __mapper_args__ = {
        'polymorphic_identity': 'organization'
    }

    ## Returns the string representation of the Organization
    # \return the string representation of the organization object
    def __str__(self):
        return "<Organization: {0}>".format(self.name)

    ## Initialize the organization Object
    # \param name the name of the organization
    def __init__(self, name, reseller):
        self.name = name
        self.reseller = reseller
        pass

    ## Get the organization
    # \param name the name of the org you want to get
    # \param vendor the vendor you want.
    # \return the organization if found
    # \raise OrganizationDoesNotExistException if an organization with name is not found
    @classmethod
    def Get(cls, name, vendor):
        org = cls.query.filter(cls.name == name).filter(cls.reseller_id == vendor.id).first()
        if org is None:
            raise OrganizationDoesNotExistException
        return org

    ## gets the user as well checks the password
    # \param email the email to get
    # \param the password to check
    # \return user a user object
    def GetUser(self, username="", email="", password=""):
        user = User.query.filter(db.or_(User.email == email, User.username == username)).filter(User.isStaff == True).first()
        if user is None:
            user = User.query.filter(User.organization == self)\
                    .filter(db.or_(User.email == email, User.username == username)).first()
            pass
        if user is None:
            return None
        if not user.checkPassword(password):
            return None
        return user

    ## Test if user is in org
    # \param username see if user name is taken
    # \email see if email is taken
    # \user test to see if actual user is in the Organization
    # \return True if the data is found else return true
    def containsUser(self, username="", email="", user=None):
        from .User import User
        usernameCount = User.query.join(Organization.users).filter(Organization.id==self.id)
        if user is None:
            usernameCount = usernameCount.filter(db.or_(User.username == username, User.email == email))
            pass
        else:
            if user.isStaff == True:
                return user
            usernameCount = usernameCount.filter(User.id == user.id)
            pass
        if usernameCount.count() > 0:
            return usernameCount.first()
        return None

    ##Creates the list that contains the ordered set of Websites and the dashboard for the dropdown menu.
    # \param website the website to put in the first positon
    # \returns the list for the dropdown menu
    def getDropDownItems(self, website):
        dropDownItems = [
            {"name": website.name, "url": "/show/{0}".format(website.id)},
            {"name": "Dashboard", "url": url_for('shuttlOrgs.dashboard', organization=self.sys_name)}
        ]
        for site in Website.query.filter(Website.organization_id == self.id, Website.id != website.id):
            dropDownItems.append({"name": site.name, "url": "/show/{0}".format(site.id)})
            pass
        return dropDownItems

    ## Create Organization Object
    # \param the name of the organization
    # \raise OrganizationExists when trying got create an organization that already exists
    @classmethod
    def Create(cls, reseller, *args, **kwargs):
        if kwargs.get("name") is not None:
            if kwargs["name"] in app.config["RESERVED_ORGANIZATONS"]:
                raise OrganizationExists
        try:
            inst = super(Organization, cls).Create(reseller=reseller, *args, **kwargs)
            return inst
        except IntegrityError:
            raise OrganizationExists
        pass

    ## Set this objects reseller to reseller
    # \param reseller the reseller for the organization
    def setReseller(self, reseller):
        self.reseller = reseller
        self.save()
        pass

    @property
    def sys_name(self):
        return self.name.replace(" ", "_")
