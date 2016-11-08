from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization
from shuttl.Models.User import User
from shuttl.Models.Website import Website

from flask.ext.script.commands import Command
from shuttl.tests.testbase import BaseTest
import shuttl

class FillDB(Command):
    "Filling the Database with mock info"

    def run(self):
        try:
            reseller = Reseller.Create(name='shuttl', _url='shuttl.local')
            # organization = Organization.Create(name="demo", reseller=reseller)
            # User.Create(organization=organization, reseller=reseller, username="nicoevergara", email="nico@shuttl.io", password="password", isActive=True)
            # User.Create(organization=organization, reseller=reseller, username="gabemorcote", email="gabe@shuttl.io", password="password", isActive=True)
            # User.Create(organization=organization, reseller=reseller, username="yosephradding", email="yoseph@shuttl.io", password="password", isActive=True)
            # Website.Create(name="mysite", organization=organization)
        except Exception as e:
            app.logger.error('Clear your database and migrate')
