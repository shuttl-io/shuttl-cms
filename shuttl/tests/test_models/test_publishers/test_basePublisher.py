import os
import random
import uuid
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import FileStorage

from shuttl import app
from shuttl.Models.FileTree.Directory import Directory
from shuttl.Models.FileTree.FileObjects.Template import Template
from shuttl.Models.FileTree.Webpage import Webpage
from shuttl.Models.Website import Website
from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization
from shuttl.tests import testbase
from shuttl.Models.Publishers.Base import BaseMock

class ContentBaseTest(testbase.BaseTest):
    def _setUp(self):
        self.testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.html")

    def test_publish(self):
        organization = Organization.Create(name="TestOrg", reseller=self.reseller)
        website = Website.Create(name="Thing", organization=organization)
        dir1 = Directory.Create(name="Something", website=website)
        dir2 = Directory.Create(name="Something2", website=website)
        dir2.addChild(dir1)
        dir3 = Directory.Create(name="Something", website=website)
        dir1.addChild(dir3)
        website.root.addChild(dir2)

        with open(self.testFilePath, "rb") as fp:
            file = FileStorage(fp)
            dir = Directory.Create(name="test", website=website)
            fileObj = Template.Create(parent=dir, file= file, name="test", website=website)
            dir3.children.append(fileObj)
            fileObj = Template.Create(parent=dir, file= file, name="test thing", website=website)
            dir3.children.append(fileObj)
            pass

        for i in range(100):
            chosenDir = random.choice([dir1, dir2, dir3, website.root])
            webpage = Webpage.Create(name=str(uuid.uuid4()), template=fileObj,website=website)
            chosenDir.addChild(webpage)
            pass

        publisher = BaseMock(name="tester", hostname="host.com")
        publisher.website = website
        publisher.save()

        website.root.publish(publisher)
        self.assertEqual(publisher.dirCount, 5)
        self.assertEqual(publisher.fileCount, 102)
        pass
