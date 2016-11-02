from flask import g
import os
from werkzeug.datastructures import FileStorage

from shuttl.Models.Website import Website
from shuttl.Models.organization import Organization
from shuttl.Models.Reseller import Reseller
from shuttl.Models.FileTree.Directory import Directory
from shuttl.Models.FileTree.FileObjects.Template import Template
from shuttl.Models.FileTree.Webpage import Webpage
from shuttl.tests import testbase
from shuttl import app
from shuttl.Models.ContentBlocks.ContentBase import ContentMock
from shuttl.Templates.Tags.Base import TagNameConflictError
from shuttl.Models.ContentBlocks.GlobalBlock import GlobalBlock

class ObtainTestCase(testbase.BaseTest):

    def _setUp(self):
        self.reseller = Reseller.Create(name ="testing", url="test2.com")
        self.organization = Organization.Create(name="TestOrg", reseller=self.reseller)
        self.website = Website.Create(name="Thing", organization=self.organization)
        g.previous = set()

        self.dir = Directory.Create(name='things1', website=self.website)
        self.website.root.addChild(self.dir)

        self.testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files/obtain", "obtain.html")
        self.testFilePath2 = os.path.join(app.config["BASE_DIR"], "shuttl/test_files/obtain", "multipleObtain.html")
        with open(self.testFilePath, 'rb') as fp:
            file = FileStorage(fp)
            self.obtains = Template.Create(parent=self.website.root, file=file, name='obtain.html', website=self.website)
            pass
        with open(self.testFilePath2, 'rb') as fp:
            file = FileStorage(fp)
            self.obtainsMulti = Template.Create(parent=self.website.root, file=file, name='multipleObtain.html', website=self.website)
            pass

        self.testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files/obtain", "obtain1.html")
        self.testFilePath2 = os.path.join(app.config["BASE_DIR"], "shuttl/test_files/obtain", "multipleobtains.html")
        pass

    def test_creation(self):
        with open(self.testFilePath, 'rb') as fp:
            file = FileStorage(fp)
            fileTemplate = Template.Create(parent=self.dir, file=file, name='testfile3', website=self.website)
            webpage = Webpage.Create(name='test_webpage', template=fileTemplate, website=self.website, parent=self.dir)
            pass
        webpage2 = Webpage.Create(name='test_webpage2', template=fileTemplate, website=self.website, parent=self.dir)

        with open(self.testFilePath2, 'rb') as fp:
            file = FileStorage(fp)
            fileTemplate = Template.Create(parent=self.dir, file=file, name='testfile4', website=self.website)
            webpage3 = Webpage.Create(name='test_webpage3', template=fileTemplate, website=self.website, parent=self.dir)
            pass
        webpage4 = Webpage.Create(name='test_webpage4', template=fileTemplate, website=self.website, parent=self.dir)

        webpage.buildContent(website=self.website)
        self.assertEquals(1, GlobalBlock.query.count())
        webpage2.buildContent(website=self.website)
        self.assertEquals(1, GlobalBlock.query.count())
        webpage3.buildContent(website=self.website)
        self.assertEquals(2, GlobalBlock.query.count())
        webpage4.buildContent(website=self.website)
        self.assertEquals(2, GlobalBlock.query.count())
        pass

    def test_build(self):
        with open(self.testFilePath, 'rb') as fp:
            file = FileStorage(fp)
            fileTemplate = Template.Create(parent=self.dir, file=file, name='testfile3', website=self.website)
            webpage = Webpage.Create(name='test_webpage', template=fileTemplate, website=self.website, parent=self.dir)
            pass
        webpage2 = Webpage.Create(name='test_webpage2', template=fileTemplate, website=self.website, parent=self.dir)

        with open(self.testFilePath2, 'rb') as fp:
            file = FileStorage(fp)
            fileTemplate = Template.Create(parent=self.dir, file=file, name='testfile4', website=self.website)
            webpage3 = Webpage.Create(name='test_webpage3', template=fileTemplate, website=self.website, parent=self.dir)
            pass
        webpage4 = Webpage.Create(name='test_webpage4', template=fileTemplate, website=self.website, parent=self.dir)

        self.assertEquals(webpage.buildContent(website=self.website), webpage2.buildContent(website=self.website))
        self.assertEquals(webpage3.buildContent(website=self.website), webpage4.buildContent(website=self.website))

        render = webpage3.buildContent(website=self.website)
        block = GlobalBlock.query.filter(GlobalBlock.template_id == self.obtains.id).first()
        block["testBlock"] = "things"
        self.assertEquals(webpage.buildContent(website=self.website), webpage2.buildContent(website=self.website))
        self.assertEquals(webpage3.buildContent(website=self.website), webpage4.buildContent(website=self.website))
        self.assertNotEquals(render, webpage4.buildContent(website=self.website))

        render = webpage.buildContent(website=self.website)
        block = GlobalBlock.query.filter(GlobalBlock.template_id == self.obtainsMulti.id).first()
        block["testBlock"] = "things"
        self.assertEquals(webpage.buildContent(website=self.website), webpage2.buildContent(website=self.website))
        self.assertEquals(render, webpage2.buildContent(website=self.website))
        self.assertEquals(webpage3.buildContent(website=self.website), webpage4.buildContent(website=self.website))




