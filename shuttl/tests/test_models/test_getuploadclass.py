from shuttl.Models.FileTree import get_upload_file_class
from shuttl.tests import testbase
from werkzeug.datastructures import FileStorage
from shuttl.Models.FileTree.FileObjects.CssFile import CssFile
from shuttl.Models.FileTree.FileObjects.FileObject import FileObject
import os
from shuttl import app

class GetUploadClassTestCase(testbase.BaseTest):

    def test_upload(self):
        self.csstestFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.css")
        with open(self.csstestFilePath, "rb") as fp:
            file = FileStorage(fp)
            cls = get_upload_file_class(file)
            self.assertEqual(cls, CssFile)

        self.texttestFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.txt")
        with open(self.texttestFilePath, "rb") as fp:
            file = FileStorage(fp)
            cls = get_upload_file_class(file)
            self.assertEqual(cls, FileObject)
        pass