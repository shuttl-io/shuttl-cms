import os
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import FileStorage

from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization
from shuttl.Models.Website import Website
from shuttl.Models.FileTree.Directory import Directory
from shuttl.Models.FileTree.FileObjects.Template import Template
from shuttl.Models.FileTree.Webpage import Webpage
from shuttl.tests import testbase
from shuttl import app
from shuttl.Models.ContentBlocks.ContentBase import ContentMock, ContentBase


class ContentBaseTest(testbase.BaseTest):

    def _setUp(self):
        self.reseller = Reseller.Create(name ="t", _url="tessss1.com")
        self.organization = Organization.Create(name="TestOrg", reseller=self.reseller)
        self.website = Website.Create(name="Thing", organization=self.organization)
        self.testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test2.html")
        with open(self.testFilePath, 'rb') as fp:
            file = FileStorage(fp)
            dir = Directory.Create(name='stuff', website=self.website)
            self.fileTemplate = Template.Create(parent=dir, file=file, name='testfile', website=self.website)

        self.testWebpage = Webpage.Create(name='test_webpage', template=self.fileTemplate, website=self.website)
        pass

    def test_create(self):
        content = ContentMock.GetOrCreate(name="test", webpage=self.testWebpage)
        content2 = ContentBase.query.filter(ContentMock.name == "test").first()
        self.assertEqual(content, content2)
        self.assertEqual(content.renderContent(None, publishing=True), "")
        self.assertRaises(IntegrityError, ContentMock.Create, name="test", webpage=self.testWebpage)
        content = ContentMock.GetOrCreate(name="test2", webpage=self.testWebpage, defaultContent="this is a test")
        self.assertNotEqual(content.renderContent(None, publishing=True), "")
        pass

    def test_rendercontent(self):
        content = ContentMock.GetOrCreate(name="test", webpage=self.testWebpage)
        self.assertEqual(content.renderContent(None, publishing=False), "<div class='testing'></div>")
        self.assertEqual(content.renderContent(None, publishing=True), "")
        pass

    def test_get(self):
        content = ContentMock.GetOrCreate(name="test", webpage=self.testWebpage)
        content2 = ContentBase.GetOrCreate(name="test", webpage=self.testWebpage)
        self.assertEqual(type(content), type(content2))
        self.assertEqual(content, content2)
        pass

    def test_setContent(self):
        content = ContentMock.GetOrCreate(name="test", webpage=self.testWebpage)
        self.assertEqual(content.renderContent(None, publishing=True), "")
        content.setContent("test")
        content = ContentMock.GetOrCreate(name="test", webpage=self.testWebpage)
        self.assertEqual(content.renderContent(None, publishing=True), "test")
        pass