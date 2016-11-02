from werkzeug.datastructures import FileStorage

from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization
from shuttl.Models.Website import Website
from shuttl.Models.FileTree.Directory import Directory
from shuttl.Models.FileTree.FileObjects.Template import Template
from shuttl.tests import testbase
import os
from shuttl import app


class TemplateTestCase(testbase.BaseTest):

    def _setUp(self):
        self.reseller = Reseller.Create(name ="testing", url="test2.com")
        self.organization = Organization.Create(name="TestOrg", reseller=self.reseller)
        self.website = Website.Create(name="Thing", organization=self.organization)
        self.testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.html")
        with open(self.testFilePath, 'rb') as fp:
            file = FileStorage(fp)
            dir = Directory.Create(name='stuff', website=self.website)
            self.website.root.addChild(dir)
            self.fileObj = Template.Create(parent=dir, file=file, name='testfile', website=self.website)

        pass

    def test_headers(self):
        self.assertEquals({'Content-Type': 'text/plain'}, self.fileObj.headers())
        pass

    def test_render(self):
        bad_render = {

        }

        good_render = {
            'id': self.fileObj.id,
            'name': self.fileObj.name,
            'type': self.fileObj.fileType,
            'sys_name': self.fileObj.sys_name
        }

        self.assertNotEquals(bad_render, self.fileObj.render())
        self.assertEquals(good_render, self.fileObj.render())
        pass

    def test_buildContent(self):
        context = {
            'dog': 'german shepard',
            'more': 'stuff'
        }

        test_results = repr('<p>\n  german shepard\n  more stuff inside\n  stuff\n</p>')
        results = self.fileObj.buildContent(context, render=True)
        self.assertEquals(repr(results), test_results)
        pass
