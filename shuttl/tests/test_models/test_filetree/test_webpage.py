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

class WebpageTestCase(testbase.BaseTest):
    def _setUp(self):
        self.reseller = Reseller.Create(name ="testing", url="test2.com")
        self.organization = Organization.Create(name="TestOrg", reseller=self.reseller)
        self.website = Website.Create(name="Thing", organization=self.organization)
        g.previous = set()
        self.testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test2.html")
        with open(self.testFilePath, 'rb') as fp:
            file = FileStorage(fp)
            dir = Directory.Create(name='things1', website=self.website)
            self.website.root.addChild(dir)
            self.fileTemplate = Template.Create(parent=dir, file=file, name='testfile', website=self.website)
        self.testWebpage = Webpage.Create(name='test_webpage', template=self.fileTemplate, website=self.website, parent=dir)
        pass

    def test_headers(self):
        self.assertEquals({'Content-Type': 'text/html'}, self.testWebpage.headers())
        pass

    def test_render(self):
        bad_render = {

        }

        good_render = {
            'id': self.testWebpage.id,
            'name': self.testWebpage.name,
            'type': self.testWebpage.fileType,
            'sys_name': self.testWebpage.sys_name
        }

        self.assertNotEquals(bad_render, self.testWebpage.render())
        self.assertEquals(good_render, self.testWebpage.render())
        pass

    def test_buildContent(self):
        test_results = '<p>\n  test_webpage\n  more stuff inside\n  page\n</p>'
        results = self.testWebpage.buildContent()
        self.assertEquals(results, test_results)
        pass

    def test_indexAccess(self):
        def tester(name):
            return self.testWebpage[name]
            pass
        content = ContentMock.GetOrCreate(name="test", webpage=self.testWebpage, defaultContent="this is a test")
        self.assertEqual(self.testWebpage["test"], content)
        self.assertEqual(self.testWebpage["test"].renderContent(None, publishing=True), "this is a test")
        self.assertRaises(IndexError, tester, "fhdjfhdjkfhak")
        self.testWebpage["test"] = "things"
        self.assertEqual(self.testWebpage["test"], content)
        self.assertEqual(self.testWebpage["test"].renderContent(None, publishing=True), "things")
        pass

    def test_wysiygTag(self):
        testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files/wysiwyg", "test_tags.html")
        with open(testFilePath, 'rb') as fp:
            file = FileStorage(fp)
            dir = Directory.Create(name='stuff', website=self.website)
            self.website.root.addChild(dir)
            fileTemplate = Template.Create(parent=dir, file=file, name='testfile', website=self.website)
            pass
        testWebpage = Webpage.Create(name='test_webpage', template=fileTemplate, website=self.website, parent=dir)
        res = testWebpage.buildContent()
        res = "".join(res.split())
        self.assertEqual(len(testWebpage.contentBlocks), 1)
        block = testWebpage.contentBlocks[0]
        expected = """
        <p>
            <shuttl-wysiwyg block="{block}" id="{page}_{block}" page="{page}" self_id="1">{content}</shuttl-wysiwyg>
        </p>
        """.format(page=testWebpage.id, block=block.name, content="")
        expected = "".join(expected.split())
        self.assertEqual(res, expected)

        testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files/wysiwyg", "test_tags_broken.html")
        with open(testFilePath, 'rb') as fp:
            file = FileStorage(fp)
            dir = Directory.Create(name='stuff2', website=self.website)
            self.website.root.addChild(dir)
            fileTemplate = Template.Create(parent=dir, file=file, name='testfile', website=self.website)
            pass
        testWebpage = Webpage.Create(name='test_webpage', template=fileTemplate, website=self.website, parent=dir)
        self.assertRaises(TagNameConflictError, testWebpage.buildContent)

        testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files/wysiwyg", "test_tags_default.html")
        with open(testFilePath, 'rb') as fp:
            file = FileStorage(fp)
            dir = Directory.Create(name='stuff3', website=self.website)
            self.website.root.addChild(dir)
            fileTemplate = Template.Create(parent=dir, file=file, name='testfile', website=self.website)
            pass
        testWebpage = Webpage.Create(name='test_webpage', template=fileTemplate, website=self.website, parent=dir)
        res = testWebpage.buildContent()
        res = "".join(res.split())
        block = testWebpage.contentBlocks[0]
        expected = """
        <p>
            <shuttl-wysiwyg block="{block}" id="{page}_{block}" page="{page}" self_id="3">{content}</shuttl-wysiwyg>
        </p>
        """.format(page=testWebpage.id, block=block.name, content="things")
        expected = "".join(expected.split())
        self.assertEqual(res, expected)
        pass
