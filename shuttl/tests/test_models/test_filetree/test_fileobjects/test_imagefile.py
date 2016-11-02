from werkzeug.datastructures import FileStorage

from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization
from shuttl.Models.Website import Website
from shuttl.Models.FileTree.Directory import Directory
from shuttl.Models.FileTree.FileObjects.ImageFile import ImageFile
from shuttl.tests import testbase
from shuttl import app
import os


class ImageFileTestCase(testbase.BaseTest):
    def _setUp(self):
        self.reseller = Reseller.Create(name="testing", _url="test2.com")
        self.organization = Organization.Create(name="TestOrg", reseller=self.reseller)
        self.website = Website.Create(name="Thing", organization=self.organization)
        self.testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.jpg")
        self.testFilePath2 = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.png")

        with open(self.testFilePath, "rb") as fp:
            file = FileStorage(fp)
            self.fileObj = ImageFile.Create(parent=self.website.root, file=file, name="test.jpg", website=self.website)
        with open(self.testFilePath2, "rb") as fp:
            file = FileStorage(fp)
            self.fileObj2 = ImageFile.Create(parent=self.website.root, file=file, name="test.png", website=self.website)
        pass

    def _readFile(self, filepath):
        content = None
        with open(filepath, "rb") as fp:
            content = fp.read()
            pass
        return content

    def test_headers(self):
        self.assertEquals({'Content-Type': 'image/jpeg'}, self.fileObj.headers())
        self.assertEquals({'Content-Type': 'image/png'}, self.fileObj2.headers())
        pass

    def test_build(self):
        fileObj = ImageFile.query.filter(ImageFile.id == self.fileObj.id).first()
        fileObj2 = ImageFile.query.filter(ImageFile.id == self.fileObj2.id).first()
        self.assertEquals(fileObj.fileExt, 'jpg')
        self.assertEquals(fileObj.name, 'test.jpg')
        self.assertEquals(fileObj2.fileExt, 'png')
        self.assertEquals(fileObj2.name, 'test.png')
        self.assertEquals(self._readFile(self.testFilePath), fileObj.buildContent())
        self.assertEquals(self._readFile(self.testFilePath2), fileObj2.buildContent())
        pass
