from flask import g
import os
import unittest
from werkzeug.datastructures import FileStorage

from shuttl.Models.FileTree.Directory import Directory
from shuttl.Models.FileTree.FileObjects.Template import Template
from shuttl.Models.FileTree.Webpage import Webpage
from shuttl.tests import testbase
from shuttl import app
from shuttl.Models.ContentBlocks.ContentBase import ContentMock
from shuttl.Templates.Tags.Base import TagNameConflictError
from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization, OrganizationDoesNotExistException
from shuttl.Models.Website import Website
from shuttl.Models.FileTree.FileObjects.CssFile import CssFile

class SiteMapTestCase(testbase.BaseTest):
    def _setUp(self):
        g.previous = set()
        self.maxDiff = None
        self.testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files")
        self.reseller = Reseller(name="test4", _url="test2.com")
        self.reseller.save()
        self.organization = Organization.Create(name="TestOrg", reseller=self.reseller)
        self.website = Website.Create(name="Thing", organization=self.organization)
        pth = os.path.join(app.config["BASE_DIR"], "shuttl/test_files/siteMap", "sitemape.html")
        with open(pth, 'rb') as fp:
            file = FileStorage(fp)
            dir = self.website.root.addChildDir("stuff", self.website)
            self.fileTemplate = Template.Create(parent=dir, file=file, name='testfile', website=self.website)
            pass
        pass

    @unittest.skipIf(app.config["SHOULD_SKIP"], reason='fix later')
    def test_build(self):
        templateRes = self.fileTemplate.buildContent(dict(website=self.website), render=True)
        expected = """
        <a href="#" class="dir">root</a>
        <ul class="directoryContainer 2 root" id="dirContainer-2">
           <li class="dir" id="dir-4">
              <a href="#" class="dir">stuff</a>
              <ul class="directoryContainer 4 " id="dirContainer-4">
                 <li class="twig" id="twig-5">
                    <a href="/show/1/5" class="twig">testfile</a>
                 </li>
                 <li class="twig" id="twig-5">
                    <a href="/show/1/5" class="twig">testfile</a>
                 </li>
              </ul>
           </li>
        </ul>
        """
        self.assertEqual(self.removeWhiteSpace(templateRes), self.removeWhiteSpace(expected))
        webpage = Webpage.Create(name='test_webpage', template=self.fileTemplate, website=self.website)
        self.website.root.addChild(webpage)
        expected = """
        <a href="#" class="dir">root</a>
        <ul class="directoryContainer 2 root" id="dirContainer-2">
           <li class="dir" id="dir-4">
              <a href="#" class="dir">stuff</a>
              <ul class="directoryContainer 4 " id="dirContainer-4">
                 <li class="twig" id="twig-5">
                    <a href="/show/1/5" class="twig">testfile</a>
                 </li>
              </ul>
           </li>
           <li class="page" id="page-6">
              <a href="/show/1/6" class="page">test_webpage</a>
           </li>
        </ul>
        """
        templateRes = self.fileTemplate.buildContent(dict(website=self.website), render=True)
        self.assertEqual(self.removeWhiteSpace(templateRes), self.removeWhiteSpace(expected))
        dir2 = Directory.Create(name="Something2", website=self.website)
        self.website.root.addChild(dir2)
        testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.css")
        with open(testFilePath, "rb") as fp:
            file = FileStorage(fp)
            file = CssFile.Create(parent=dir2, file=file, name="test", website=self.website)
            file.save()
            dir = Directory.Create(name="testDir", website=self.website)
            dir2.addChild(dir)
            pass
        webpage = Webpage.Create(name='test_webpage2', template=self.fileTemplate, website=self.website)
        dir.addChild(webpage)
        expected = """
        <a href="#" class="dir">root</a>
        <ul class="directoryContainer [0-9] root" id="dirContainer-[0-9]">
           <li class="dir" id="dir-[0-9]">
              <a href="#" class="dir">Something2</a>
              <ul class="directoryContainer [0-9] " id="dirContainer-[0-9]">
                 <li class="css" id="css-[0-9]">
                    <a href="/show/1/[0-9]" class="css">test</a>
                 </li>
                 <li class="dir" id="dir-[0-9]">
                    <a href="#" class="dir">testDir</a>
                    <ul class="directoryContainer [0-9] " id="dirContainer-[0-9]">
                       <li class="page" id="page-[0-9][0-9]">
                          <a href="/show/1/[0-9][0-9]" class="page">test_webpage2</a>
                       </li>
                    </ul>
                 </li>
              </ul>
           </li>
           <li class="dir" id="dir-[0-9]">
              <a href="#" class="dir">stuff</a>
              <ul class="directoryContainer [0-9] " id="dirContainer-[0-9]">
                 <li class="twig" id="twig-[0-9]">
                    <a href="/show/1/[0-9]" class="twig">testfile</a>
                 </li>
              </ul>
           </li>
           <li class="page" id="page-[0-9]">
              <a href="/show/1/[0-9]" class="page">test_webpage</a>
           </li>
        </ul>
        """
        templateRes = self.fileTemplate.buildContent(dict(website=self.website), render=True)
        self.assertRegex(self.removeWhiteSpace(templateRes), self.removeWhiteSpace(expected))
        pass
