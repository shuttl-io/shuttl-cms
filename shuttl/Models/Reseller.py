from flask import request

from shuttl import app
from shuttl.database import BaseModel, db
from shuttl.Models.User import User

class ResellerDoesNotExist(Exception): pass

## Model for the reseller
class Reseller(BaseModel, db.Model):
    ## name of the reseller
    name = db.Column(db.String, unique=True, nullable=False)

    ## URL of the reseller's website
    _url = db.Column(db.String, unique=True, nullable=False)

    ##The Directory to be on.
    directory = db.Column(db.String, default="")

    ## the subdirectory that shuttl is hosted on. This is for reverse proxies
    subdir = db.Column(db.String, default="")

    ## Organizations Managed by this reseller
    organizations = db.relationship("Organization", back_populates='reseller', lazy='dynamic')

    ## Organizations Managed by this reseller
    admins = db.relationship("User", backref='reseller', lazy='dynamic')

    ## The pricing this reseller wants to charge
    _price = db.Column(db.Float, default=app.config["BASEPRICE"])

    ## Gets all of the Contacts for this reseller
    @property
    def contacts(self):
        return User.query.filter(User.reseller_id == self.id, User.isContact == True)

    ## gets the pricing
    @property
    def price(self):
        return self._price

    ## Sets the price, but makes sure it is above a value
    # \param new the new price
    @price.setter
    def price(self, new):
        self._price = new
        if new > app.config["BASEPRICE"]:
            self.save()
            pass
        pass

    ## Adds an organization to the vendor
    # \param organization the organization to add to this reseller
    def addOrganization(self, organization):
        organization.setReseller(self)
        pass

    ## Adds an admin to the vendor
    # \param admin the user to add to this vendor
    def addAdmin(self, admin):
        self.admins.append(admin)
        self.save()
        pass

    ## Gets the vendor from hostname
    # \param hostname the hostname to get
    # \return the vendor how has the hostname
    # \raises ResellerDoesNotExist if the reseller doesn't exist
    @classmethod
    def GetFromHostname(cls, hostname):
        reseller = Reseller.query.filter(Reseller._url == hostname).first()
        if reseller is None:
            raise ResellerDoesNotExist
        return reseller

    @property
    def url(self):
        return "http://{0}/{1}".format(self._url, self.directory)

    @url.setter
    def url(self, newUrl):
        self._url = newUrl
        pass

    ## gets the user as well checks the password
    # \param username the username to get
    # \param the password to check
    def GetUser(self, username="", password=""):
        user = User.query.filter(User.reseller_id==self.id).filter(User.username == username).first()
        if user is None:
            return None
        if not user.checkPassword(password):
            return None
        return user

    ## Gets the hostname from the string
    # \param host the actual host header value
    # \return the hostname with just the Domain
    @classmethod
    def GetNameFromHost(cls, host):
        hostname = request.headers.get("host")
        if hostname is None:
            return '105 error', 105
        hostname = hostname.split("//", 1)[-1]
        hostname = hostname.split("/")[0]
        hostname = hostname.rsplit(":", 1)[0]
        hostname = hostname.split(".")

        ## The first part may be an organization name, or it could be part of the url. better try both.
        hostname1 = ".".join(hostname[1:])
        hostname2 = ".".join(hostname)
        reseller = None
        try:
            reseller = cls.GetFromHostname(hostname1)
            pass
        except ResellerDoesNotExist:
            reseller = cls.GetFromHostname(hostname2)
            pass
        return reseller


