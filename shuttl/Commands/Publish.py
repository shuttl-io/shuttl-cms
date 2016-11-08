import os
from flask.ext.script.commands import Command, Option
import sys
import getpass

from shuttl import app
from shuttl.Models.User import User
from shuttl.Models.organization import Organization
from shuttl.Models.Reseller import Reseller
from shuttl.Models.Website import Website


## TestSuite for running test modules from command line
# \param Command The command that is input from command line
class Publish(Command):
    "Testing components of your application"

    option_list = (
        Option('-w', '--website', dest="website")
    )

    def run(self, website):
        if website is None:
            website = print("Website Name:")
            pass
        website = Website.query.filter(Website.name==website).first()
        if website is None:
            print("Website does not exsist")
            return
        website.publish()
        pass


