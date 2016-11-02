from flask import g
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
from shuttl.Models.ContentBlocks.ContentBase import ContentMock
from shuttl.Templates.Tags.Base import TagNameConflictError
from shuttl.Models.ContentBlocks.MultipleBlock import MultipleBlock
from shuttl.Models.ContentBlocks.MultipleContent import MultipleContent

class MultiBlockTestCase(testbase.BaseTest):

    def _setUp(self):
        self.reseller = Reseller.Create(name ="testing", url="test2.com")
        self.organization = Organization.Create(name="TestOrg", reseller=self.reseller)
        self.website = Website.Create(name="Thing", organization=self.organization)
        g.previous = set()
        self.testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test2.html")
        with open(self.testFilePath, 'rb') as fp:
            file = FileStorage(fp)
            dir = Directory.Create(name='things1', website=self.website)
            self.website.root.addChild(dir)
            self.fileTemplate = Template.Create(parent=dir, file=file, name='testfile', website=self.website)
        self.webpage = Webpage.Create(name='test_webpage', template=self.fileTemplate, website=self.website, parent=dir)
        self.maxDiff = None
        pass

    def compileTemplate(self, templateStr):
        ast = app.jinja_env._parse(templateStr, "testing_multiblock", "testing_multiblock")
        generator = app.jinja_env.code_generator_class(app.jinja_env, 
            "testing_multiblock", 
            "testing_multiblock"
        )
        generator.visit(ast)
        return generator.stream.getvalue()


    def test_creation(self):
        templateStr = """
        <div class = "multipleItem">Things</div>
        """
        templateStr = self.compileTemplate(templateStr)
        multi = MultipleBlock.GetOrCreate("test", self.webpage, templateStr)
        self.assertEquals(1, MultipleBlock.query.count())
        self.assertEquals(1, MultipleContent.query.count())
        self.assertEquals(type(multi), MultipleBlock)
        multi2 = MultipleBlock.GetOrCreate("test", self.webpage, templateStr)
        self.assertEqual(multi, multi2)
        pass

    def test_listBehaviour(self):
        templateStr = """
        <div class = "multipleItem">Things</div>
        """
        templateStr = self.compileTemplate(templateStr)
        multi = MultipleBlock.GetOrCreate("test", self.webpage, templateStr)
        m2 = multi.append()
        m3 = multi.append()
        m1 = multi.firstContent
        self.assertEquals(3, MultipleContent.query.count())
        count = 0
        for block in multi:
            count += 1
            pass
        self.assertEqual(3, count)
        self.assertEqual(3, len(multi))
        obj = multi[0]
        obj2 = multi[1]
        obj3 = multi[2]
        self.assertEqual(obj, m1)
        self.assertEqual(obj2, m2)
        self.assertEqual(obj3, m3)
        self.assertRaises(IndexError, multi.__getitem__, 3)
        index = 0
        id_ = 7
        for block in multi:
            self.assertEqual(index, block.index)
            self.assertEqual(id_, block.id)
            index += 1
            id_ += 1
            pass
        pass

    def test_render(self):
        templateStr = """
        <div class = "multipleItem">Things</div>
        """
        templateStr = self.compileTemplate(templateStr)
        multi = MultipleBlock.GetOrCreate("test", self.webpage, templateStr)
        m2 = multi.append()
        m3 = multi.append()
        m1 = multi.firstContent
        proper = """
            <shuttl-multiblock page="6" block="test" id="1">
                            <shuttl-multiItem self_id="7" index="0" owner="test">
                <div class="multipleItem">Things</div>
                </shuttl-multiItem>

                            <shuttl-multiItem self_id="8" index="1" owner="test">
                <div class="multipleItem">Things</div>
                </shuttl-multiItem>

                            <shuttl-multiItem self_id="9" index="2" owner="test">
                <div class="multipleItem">Things</div>
                </shuttl-multiItem>
            </shuttl-multiblock>
        """
        self.assertEqual(self.removeWhiteSpace(proper), self.removeWhiteSpace(multi.renderContent(dict())))

        templateStr2 = """
        <div class = "multipleItem"><h1>Hello</h1>Things2</div>
        """

        templateStr2 = self.compileTemplate(templateStr2)
        multi.templateCompiled = templateStr2
        multi.save()

        proper = """
            <shuttl-multiblock page="6" block="test" id="1">
            <shuttl-multiItem self_id="7" index="0" owner="test">
<div class="multipleItem"><h1>Hello</h1>Things2</div>
</shuttl-multiItem>

            <shuttl-multiItem self_id="8" index="1" owner="test">
<div class="multipleItem"><h1>Hello</h1>Things2</div>
</shuttl-multiItem>

            <shuttl-multiItem self_id="9" index="2" owner="test">
<div class="multipleItem"><h1>Hello</h1>Things2</div>
</shuttl-multiItem>
            </shuttl-multiblock>
        """
        self.assertEqual(self.removeWhiteSpace(proper), self.removeWhiteSpace(multi.renderContent(dict())))
        pass

    def test_Move(self):
        templateStr = """
        <div class = "multipleItem">Things</div>
        """
        templateStr = self.compileTemplate(templateStr)
        multi = MultipleBlock.GetOrCreate("test", self.webpage, templateStr)
        m2 = multi.append()
        m3 = multi.append()
        m1 = multi.firstContent

        m3.moveUp()
        count = 0
        for i in multi:
            count += 1
            if count > 10:
                break
            pass
        self.assertEqual(3, count)
        self.assertEqual(m3, multi[1])

        m3.moveDown()
        count = 0
        for i in multi:
            count += 1
            if count > 10:
                break
            pass
        self.assertEqual(3, count)
        self.assertEqual(m3, multi[2])

        m3.moveDown()
        count = 0
        for i in multi:
            count += 1
            if count > 10:
                break
            pass
        self.assertEqual(3, count)
        self.assertEqual(m3, multi[2])
        pass

    def test_big(self):
        templateStr = """
        <div class = "multipleItem">Things</div>
        """
        templateStr = self.compileTemplate(templateStr)
        multi = MultipleBlock.GetOrCreate("test", self.webpage, templateStr)
        for i in range(19):
            multi.append()
            pass
        ndx = 0
        _id = multi.firstContent.id
        self.assertEqual(20, len(multi))
        for i in multi:
            self.assertEqual(_id, i.id)
            self.assertEqual(ndx, i.index)
            _id += 1
            ndx += 1
            pass
        multi.pop(10)
        self.assertEqual(19, len(multi))

        ndx = 0
        for i in multi:
            self.assertEqual(ndx, i.index)
            ndx += 1
            pass
        pass
