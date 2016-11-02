from werkzeug.datastructures import FileStorage

from shuttl.Models.FileTree.FileObjects.FileObject import FileObjectMock
from shuttl.Models.FileTree.TreeNodeObject import BrokenPathError
from shuttl.Models.FileTree.FileObjects.FileObject import FileObject
from shuttl.Models.Website import Website
from shuttl.Models.organization import Organization
from shuttl.Models.FileTree.Directory import Directory
from shuttl.tests import testbase
from shuttl import app
import os
from shuttl.Models.Reseller import Reseller


class FileObjectTestCase(testbase.BaseTest):
    def _setUp(self):
        self.reseller = Reseller.Create(name="test4", _url="test2.com")
        self.organization = Organization.Create(name="TestOr", reseller=self.reseller)
        self.website = Website.Create(name="Thing", organization=self.organization)
        self.testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.txt")
        pass

    def _readFile(self):
        content = None
        with open(self.testFilePath, "w+") as fp:
            content = fp.read()
            pass
        return content

    def test_create(self):
        with open(self.testFilePath, "rb") as fp:
            file = FileStorage(fp)
            dir = Directory.Create(name="test", website=self.website)
            file_dictionary = {n._fileType: n for n in FileObject.__subclasses__()}
            fileObj = FileObjectMock.Create(parent=dir, file=file, name="test", website=self.website)
            fileObj2 = FileObjectMock.query.get(fileObj.id)
            self.assertEqual(fileObj, fileObj2)
            self.assertEqual(fileObj.sys_name, fileObj.name)
            fileObj = FileObjectMock.Create(parent=dir, file=file, name="test thing", website=self.website)
            self.assertNotEqual(fileObj.sys_name, fileObj.name)
            self.assertEqual(fileObj.sys_name, fileObj.name.replace(" ", "_"))
            pass
        pass

    def test_file(self):
        content = self._readFile()
        with open(self.testFilePath, "rb") as fp:
            file = FileStorage(fp)
            dir = Directory.Create(name="test", website=self.website)
            fileObj = FileObjectMock.Create(parent=dir, file=file, name="test", website=self.website)
            self.assertEqual(content, fileObj.file.read())
            fileObj.writeToFile("This is a cool test \nwhat?")
            content = self._readFile()
            self.assertNotEqual(content, fileObj.file.read())
            pass
        pass

    def test_getUploadPath(self):
        with open(self.testFilePath, "rb") as fp:
            file = FileStorage(fp)
            dir = Directory.Create(name="test", website=self.website)
            fileObj = FileObjectMock.Create(parent=dir, file=file, name="test", website=self.website)
            pass
        self.assertEqual(fileObj.getUploadPath(), app.config["UPLOAD_DIR"])

        pass

    def test_getfilefrompath(self):
        organization = Organization.Create(name="TestOrg", reseller=self.reseller)
        website = Website.Create(name="Thing", organization=organization)
        dir = website.root.addChildDir(name="test", website=website).addChildDir(name="test2", website=website).addChildDir(name="test3", website=website)
        with open(self.testFilePath, "rb") as fp:
            file = FileStorage(fp)
            fileObj = FileObjectMock.Create(parent=dir, file=file, name="test.html", website=website)
            pass
        fileObj2 = FileObject.GetFileFromPath("/test/test2/test3/test.html", website)
        self.assertEqual(fileObj2, fileObj)
        self.assertEqual(type(fileObj2), type(fileObj))

        self.assertRaises(BrokenPathError, FileObject.GetFileFromPath, "/test/tes2/test3/test.html", website)
        self.assertRaises(FileNotFoundError, FileObject.GetFileFromPath, "/test/test2/test3/teft.html", website)
        pass

    def test_fullpath(self):
        organization = Organization.Create(name="TestOrg", reseller=self.reseller)
        website = Website.Create(name="Thing", organization=organization)
        dir = website.root.addChildDir(name="test", website=website).addChildDir(name="test2", website=website).addChildDir(name="test3", website=website)
        with open(self.testFilePath, "rb") as fp:
            file = FileStorage(fp)
            fileObj = FileObjectMock.Create(parent=dir, file=file, name="test.html", website=self.website)
            pass
        self.assertEqual(fileObj.fullPath, "/test/test2/test3/test.html")
        pass

    def test_delete(self):
        def test(fileObj):
            return fileObj.file

        organization = Organization.Create(name="TestOrg", reseller=self.reseller)
        website = Website.Create(name="Thing", organization=organization)
        dir = website.root.addChildDir(name="test", website=website).addChildDir(name="test2", website=website).addChildDir(name="test3", website=website)
        with open(self.testFilePath, "rb") as fp:
            file = FileStorage(fp)
            fileObj = FileObjectMock.Create(parent=dir, file=file, name="test.html", website=website)
            pass
        fileObj.delete(removeFile=True)
        self.assertRaises(FileNotFoundError, test, fileObj)
        pass
