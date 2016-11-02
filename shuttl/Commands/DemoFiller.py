from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization
from shuttl.Models.User import User
from shuttl.Models.Website import Website
from shuttl.Models.FileTree.Directory import Directory
from shuttl.Models.FileTree.FileObjects.CssFile import CssFile
from shuttl.Models.FileTree.FileObjects.Template import Template
from shuttl.Models.FileTree.Webpage import Webpage

from werkzeug.datastructures import FileStorage
from flask.ext.script.commands import Command
from shuttl.tests.testbase import BaseTest
import shuttl
import os

class DemoFiller(Command):
    "Filling the Database with mock info"

    def run(self):
        try:
            BaseTest.clear_data(shuttl.db.session)
            reseller = Reseller.Create(name='shuttl', _url='shuttl.com')
            organization = Organization.Create(name="demo", reseller=reseller)
            website = Website.Create(name="demo-site", organization=organization)
            cssfile = os.path.join(shuttl.app.config["BASE_DIR"], "shuttl/demo_files/css/style.css")
            templatefile = os.path.join(shuttl.app.config["BASE_DIR"], "shuttl/demo_files/index.html")
            with open(cssfile, "rb") as fp:
                file = FileStorage(fp)
                CssFile.Create(website=website, parent=website.root, name="style.css", file=file)
                pass

            with open(templatefile, "rb") as fp:
                file = FileStorage(fp)
                self.template = Template.Create(website=website, parent=website.root, name="index.html", file=file)
                pass

            Webpage.Create(template=self.template, website=website, parent=website.root, name="index")


        except Exception as e:
            app.logger.error('Clear your database and migrate')
