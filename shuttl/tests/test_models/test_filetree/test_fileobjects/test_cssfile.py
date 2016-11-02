from werkzeug.datastructures import FileStorage

from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization
from shuttl.Models.Website import Website
from shuttl.Models.FileTree.Directory import Directory
from shuttl.Models.FileTree.FileObjects.CssFile import CssFile
from shuttl.tests import testbase
from shuttl import app
import os


class CssFileTestCase(testbase.BaseTest):
    def _setUp(self):
        self.reseller = Reseller.Create(name="testing", _url="test2.com")
        self.organization = Organization.Create(name="TestOrgcss", reseller=self.reseller)
        self.website = Website.Create(name="Thing", organization=self.organization)
        self.testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.css")

        with open(self.testFilePath, "rb") as fp:
            file = FileStorage(fp)
            self.fileObj = CssFile.Create(parent=self.website.root, file=file, name="test", website=self.website)
            self.fileObj2 = CssFile.Create(parent=self.website.root, file=file, name="tested", website=self.website)
        pass

    def _readFile(self):
        content = None
        with open(self.testFilePath, "r+") as fp:
            content = fp.read()
            pass
        return content

    def test_build(self):
        self.assertEqual(self._readFile(), self.fileObj.buildContent())
        pass
