import os
from werkzeug.datastructures import FileStorage

from shuttl.Models.FileTree.Directory import Directory
from shuttl.Models.FileTree.FileObjects.Template import Template
from shuttl.Models.FileTree.Webpage import Webpage
from shuttl.tests import testbase
from shuttl import app
from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization
from shuttl.Models.Website import Website
from shuttl.Models.FileTree.FileObjects.CssFile import CssFile
from shuttl.Models.FileTree.FileObjects.JsFile import JsFile
import unittest


class FileTagTestCase(testbase.BaseTest):

    @unittest.skipIf(app.config["SHOULD_SKIP"], reason='passed locally')
    def test_filetag(self):
        self.organization = Organization.Create(name="test", reseller=self.reseller)
        self.website = Website.Create(name="Thing", organization=self.organization)
        testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files/file_tag", "file_tag.html")
        testCssPath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.css")
        testJsPath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.js")

        with open(testFilePath, 'rb') as fp:
            file = FileStorage(fp)
            dir = Directory.Create(name='stuff', website=self.website)
            self.website.root.addChild(dir)
            fileTemplate = Template.Create(parent=dir, file=file, name='testfile', website=self.website)
            pass

        with open(testCssPath, 'rb') as fp:
            file2 = FileStorage(fp)
            cssFile = CssFile.Create(parent=dir, file=file2, name="style.css", website=self.website)

        with open(testJsPath, 'rb') as fp:
            file3 = FileStorage(fp)
            jsFile = JsFile.Create(parent=dir, file=file3, name="app.js", website=self.website)

        testWebpage = Webpage.Create(name='test_webpage', template=fileTemplate, website=self.website)
        res = testWebpage.buildContent(website=self.website)
        expected = """
        <link href="http://test.shuttl.com:5000/getStaticContent/6" rel="stylesheet" type="text/css"/>
        <script src="http://test.shuttl.com:5000/getStaticContent/7" type="text/javascript"></script>
        """
        self.assertEquals(self.removeWhiteSpace(res), self.removeWhiteSpace(expected))
        result = self.app.get('http://test.shuttl.com:5000/getStaticContent/6')
        self.assertEquals(result.status_code, 200)
        self.assertEquals(('Content-Type', 'text/css; charset=utf-8'), result.headers[1])
        self.assertEquals(self.removeWhiteSpace(result.data.decode()), self.removeWhiteSpace('p{\n    text-align: center;\n}'))
        result = self.app.get('http://test.shuttl.com:5000/getStaticContent/7')
        self.assertEquals(result.status_code, 200)
        self.assertEquals(('Content-Type', 'application/javascript'), result.headers[1])
        self.assertEquals(result.data.decode(), 'console.log();')
        result = self.app.get('http://test.shuttl.com:5000/getStaticContent/8')
        self.assertEquals(result.status_code, 404)
        pass
