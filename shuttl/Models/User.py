import sendgrid
import os
from flask import render_template
import random
from sendgrid.helpers.mail import Email, Content, Mail
from shuttl import app

from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from .Validators.OrganizationValidator import OrganizationValidator
from shuttl.database import BaseModel, db
from shuttl.MailChimp import MailChimp


class UserDataTakenException(Exception):
    def __init__(self, code, *args, **kwargs):
        super(UserDataTakenException, self).__init__(*args, **kwargs)
        self.code = code
        pass

class ToManyOrganizations(Exception): pass
class NoOrganizationException(Exception): pass


## Class for the user models
#
class User(BaseModel, db.Model):
    username = db.Column(db.String(), nullable=False)   ##< User's user name
    firstName = db.Column(db.String(200))  ##< User's first name
    lastName = db.Column(db.String(200))   ##< User's last name
    email = db.Column(db.String(255), nullable=False) ##< User's email address
    isActive = db.Column(db.Boolean, default=False)  ##< If the user is active, set to true after email is validated
    password = db.Column(db.String(255), nullable=False)  ##<the password of the user
    isAdmin = db.Column(db.Boolean, default=False)  ##< denotes if the user is admin
    ## If the user is a freelancer or dev shop, this allows them to be in more than one group
    isFree = db.Column(db.Boolean, default=False)
    ## Organizations the user belongs to, can be more than one if isFree is true
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    organization = db.relationship("Organization", foreign_keys=[organization_id], back_populates='users')

    ## The Github Access Token that will be associated with this User
    githubAccessToken = db.Column(db.String(), nullable=True)

    ##reseller this can belong to
    reseller_id = db.Column(db.Integer, db.ForeignKey('reseller.id'))

    ## Indicates if this user is a point of contact
    isContact = db.Column(db.Boolean, default=False)

    isStaff = db.Column(db.Boolean, default=False)

    __table_args__ = (
        db.UniqueConstraint('username', 'organization_id', name='_username_organization_id_uc'),
    )

    # ## The reseller this user belongs to.
    # reseller = db.relationship("Reseller", back_populates="admins", lazy=True)

    def __init__(self, username, email, firstName="", lastName="", isActive=False, isAdmin=False, isFree=False, reseller=None):
        self.username = username
        self.email = email
        self.firstName = self.firstName
        self.lastName = self.lastName
        self.isAdmin = isAdmin
        self.isActive = isActive
        self.isFree = isFree
        self.reseller = reseller
        pass

    @property
    def __json__(self):
        json = super(User, self).__json__
        json.remove("password")
        return json

    ## sets the password fo the user. Always use this to set passwords
    # \param newPassword the user's new password
    def setPassword(self, newPassword):
        self.password = generate_password_hash(newPassword)
        pass

    ## Checks to make sure the passowrd is correct
    # \param password the password to validate
    # \return true if this is the right password, false otherwise.
    def checkPassword(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.isActive

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @classmethod
    def Create(cls, organization=None, password="", *args, **kwargs):
        newUser = User(*args, **kwargs)
        newUser.setPassword(password)
        if organization is not None:
            if organization.containsUser(email=newUser.email):
                raise UserDataTakenException(code=-2)
            if organization.containsUser(username=newUser.username):
                raise UserDataTakenException(code=-1)
            newUser.organization = organization
            pass
        try:
            newUser.save()
        except IntegrityError:
            raise UserDataTakenException(code=-3)
        MailChimp.AddUserToList(newUser.email, newUser.firstName, newUser.lastName)
        return newUser

    ## Saves a user to the database. Makes sure they belong somewhere first.
    def save(self):
        if self.organization is None and not self.reseller and not self.isFree:
            raise NoOrganizationException()
        super(User, self).save()
        pass

    ## Sends the welcome email as well as the verify email
    def sendVerifyMessage(self):
        validator = None
        if self.organization:
            validator = OrganizationValidator.Create(self)
            pass
        url = validator.getUrl(self.organization.sys_name)
        details = dict(
            url=url,
            user=self,
            base_url="http://{0}.{1}".format(self.organization.sys_name, app.config['SERVER_NAME']),
            title="Welcome to Shuttl"
        )
        validationMsg = render_template("Email/validation.html", **details)
        fromEmail = "The Shuttl Team <hello@shuttl.io>"
        self.emailUser("Please verify your email!", fromEmail, validationMsg)
        pass

    def sendHelloEmail(self):
        support = random.choice([
            {"name": "Yoseph", "email": "yoseph@shuttl.io"},
            {"name": "Nico", "email": "nico@shuttl.io"},
            {"name": "Gabe", "email": "gabe@shuttl.io"}
        ])
        details = dict(
            user=self,
            support=support,
            base_url="http://{0}.{1}".format(self.organization.sys_name, app.config['SERVER_NAME']),
            title="Welcome to Shuttl"
        )
        helloMsg = render_template("Email/welcome.html", **details)
        fromEmail = "The Shuttl Team <hello@shuttl.io>"
        self.emailUser("Welcome to Shuttl!", fromEmail, helloMsg)
        pass

    ## emails the user
    # \param subject the subject of the email
    # \param from the user that sent this email
    # \param msg the mesage to send to the user
    def emailUser(self, subject, fro, msg):
        from shuttl import app
        sg = sendgrid.SendGridAPIClient(apikey=app.config["SENDGRID_APIKEY"])
        to_email = Email(self.email)
        from_email = Email("The Shuttl Team <hello@shuttl.io>")
        content = Content("text/html", msg)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        pass
