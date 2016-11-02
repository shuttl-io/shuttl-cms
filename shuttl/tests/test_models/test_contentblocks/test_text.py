import jinja2
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
from shuttl.Models.ContentBlocks.Text import TextBlock


class TextBaseTest(testbase.BaseTest):
     def _setUp(self):
        self.reseller = Reseller.Create(name ="testing", url="test2.com")
        self.organization = Organization.Create(name="TestOrg", reseller=self.reseller)
        self.website = Website.Create(name="Thing", organization=self.organization)
        self.testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test2.html")
        with open(self.testFilePath, 'rb') as fp:
            file = FileStorage(fp)
            dir = Directory.Create(name='stuff', website=self.website)
            self.fileTemplate = Template.Create(parent=dir, file=file, name='testfile', website=self.website)

        self.testWebpage = Webpage.Create(name='test_webpage', template=self.fileTemplate, website=self.website)
        pass

     def test_content(self):
         content = TextBlock.GetOrCreate(name="test", webpage=self.testWebpage)
         self.assertEqual(content.renderContent(None, publishing=True), "")
         content.setContent("<div>test</div>")
         self.assertEqual(content.renderContent(None, publishing=True), jinja2.escape("<div>test</div>"))
         pass