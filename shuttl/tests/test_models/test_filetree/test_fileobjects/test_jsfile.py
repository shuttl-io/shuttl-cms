from werkzeug.datastructures import FileStorage

from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization
from shuttl.Models.Website import Website
from shuttl.Models.FileTree.Directory import Directory
from shuttl.Models.FileTree.FileObjects.JsFile import JsFile
from shuttl.tests import testbase
from shuttl import app
import os


class JsFileTestCase(testbase.BaseTest):
    def _setUp(self):
        self.reseller = Reseller.Create(name ="testing", url="test2.com")
        self.organization = Organization.Create(name="TestOrg", reseller=self.reseller)
        self.website = Website.Create(name="Thing", organization=self.organization)
        self.testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.js")
        with open(self.testFilePath, "rb") as fp:
            file = FileStorage(fp)
            dir = Directory.Create(name="test", website=self.website)
            self.fileObj = JsFile.Create(parent=dir, file=file, name="test", website=self.website)
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

    def test_headers(self):
        self.assertEqual({"Content-Type": "application/javascript"}, self.fileObj.headers())
        pass

    def test_render(self):
        test = {
            "id": self.fileObj.id,
            "name": self.fileObj.name,
            "type": self.fileObj.fileType,
            "sys_name": self.fileObj.sys_name
        }
        self.assertEqual(test, self.fileObj.render())
        pass


