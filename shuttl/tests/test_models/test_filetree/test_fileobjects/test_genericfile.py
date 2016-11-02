from werkzeug.datastructures import FileStorage

from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization
from shuttl.Models.Website import Website
from shuttl.Models.FileTree.Directory import Directory
from shuttl.Models.FileTree.FileObjects.GenericFile import GenericFile
from shuttl.tests import testbase
from shuttl import app
import os


class GenericFileTestCase(testbase.BaseTest):
    def _setUp(self):
        self.reseller = Reseller.Create(name="testing", _url="test2.com")
        self.organization = Organization.Create(name="TestOrgcss", reseller=self.reseller)
        self.website = Website.Create(name="Thing", organization=self.organization)
        self.testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.cname")
        self.testFilePath2 = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.exs")

        with open(self.testFilePath, "rb") as fp:
            file = FileStorage(fp)
            self.fileObj = GenericFile.Create(parent=self.website.root, file=file, name="CNAME", website=self.website)
        with open(self.testFilePath2, "rb") as fp:
            file = FileStorage(fp)
            self.fileObj2 = GenericFile.Create(parent=self.website.root, file=file, name="test.exs", website=self.website)
        pass

    def _readFile(self, filepath):
        content = None
        with open(filepath, "r+") as fp:
            content = fp.read()
            pass
        return content

    def test_build(self):
        fileObj = GenericFile.query.filter(GenericFile.id == self.fileObj.id).first()
        fileObj2 = GenericFile.query.filter(GenericFile.id == self.fileObj2.id).first()
        self.assertEquals(fileObj.fileExt, '')
        self.assertEquals(fileObj.name, 'CNAME')
        self.assertEquals(fileObj2.fileExt, 'exs')
        self.assertEquals(self._readFile(self.testFilePath), fileObj.buildContent())
        self.assertEquals(self._readFile(self.testFilePath2), fileObj2.buildContent())
        pass
