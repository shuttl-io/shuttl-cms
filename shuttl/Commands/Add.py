import os
from flask.ext.script.commands import Command, Option
import sys
import getpass

from shuttl import app
from shuttl.Models.User import User
from shuttl.Models.organization import Organization
from shuttl.Models.Reseller import Reseller
from shuttl.Models.Website import Website
from shuttl.Models.Publishers.GitPublisher import GitPublisher
from shuttl.Models.Publishers.S3Publisher import S3Publisher

## TestSuite for running test modules from command line
# \param Command The command that is input from command line
class Add(Command):
    "Testing components of your application"

    option_list = (
        Option('-o', '--organization', dest='orgName'),
        Option('-t', '--transport', dest='transport'),
        Option('-u', '--user', dest="user"),
        Option('-w', '--website', dest="website")
    )

    def run(self, orgName, transport, user, website):
        if user:
            return self._makeUser(orgName, user)
        if orgName:
            return self._makeOrg(orgName)
        if transport:
            return self._makeTransport(transport, website)
        pass

    def _makeOrg(self, orgName):
        reseller = Reseller.query.filter(Reseller.name=="shuttl")
        orginization = Organization.Create(name=orgName, reseller=reseller)
        userEmail = input("Please enter a user email:")
        userName = input("Please enter a user name:")
        password = getpass.getpass()
        user = User.Create(
            organization=organization, 
            reseller=reseller, 
            username=userName, 
            email=userEmail, 
            password=password, 
            isActive=True
        )
        user.save()
        organization.save()
        reseller.save()
        pass

    def _makeUser(self, orgName, userEmail):
        if orgName is None:
            print ("Organization Name:")
            pass 
        if userEmail is None:
            userEmail = input("Please enter a user email:")
            pass
        reseller = Reseller.query.filter(Reseller.name=="shuttl")
        organization = Organization.query.filter(Organization.name==orgName)
        if organization is None:
            print ("That organization does not exsist. Please create it using run.py add --organization <orgName>")
            return
        userName = input("Please enter a user name:")
        password = getpass.getpass()
        user = User.Create(
            organization=organization, 
            reseller=reseller, 
            username=userName, 
            email=userEmail, 
            password=password, 
            isActive=True
        )
        user.save()
        organization.save()
        reseller.save()
        pass

    def _makeTransport(self, transport, website):
        if transport is None or transport not in {"git", "s3"}:
            print ("Please provide a transport protocol (git or s3) using -t or --transport!")
            return
        if transport == "git":
            name = input("Name:")
            relativeUrl = input("Enter relative url (defaults to '/'):")
            relativeUrl = relativeUrl or "/"
            hostname = input("Git URL:")
            privateKeyPath = input("Enter Path to the Private key:")
            if website is None:
                website = input("Website Name:")
                pass
            website = Website.query.filter(Website.name==website)
            transport = GitPublisher.Create(
                privateKeyPath=privateKeyPath,
                website=website,
                name=name,
                relativeUrl=relativeUrl,
                hostname=hostname,
            )
            transport.save()
            website.save()
        else:
            name = input("Name:")
            relativeUrl = input("Enter relative url (defaults to '/'):")
            relativeUrl = relativeUrl or "/"
            hostname = input("Git URL:")
            bucketName = input("Enter Bucket Name:")
            if website is None:
                website = input("Website Name:")
                pass
            website = Website.query.filter(Website.name==website)
            transport = S3Publisher.Create(
                bucketName=bucketName,
                website=website,
                name=name,
                relativeUrl=relativeUrl,
                hostname=hostname,
            )
            transport.save()
            website.save()
            pass
            



