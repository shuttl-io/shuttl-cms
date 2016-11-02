from sqlalchemy.exc import IntegrityError

from shuttl.Models.FileTree.Directory import Directory
from shuttl.tests import testbase
from shuttl.Models.Website import Website
from shuttl.Models.organization import Organization
from shuttl.Models.Reseller import Reseller


class DirectoryTestCase(testbase.BaseTest):

    def _setUp(self):
        self.reseller = Reseller.Create(name ="testing", _url="test2.com")
        self.organization = Organization.Create(name="TestOrg", reseller=self.reseller)
        self.website = Website.Create(name="Thing", organization=self.organization)

    def test_addChild(self):
        root = Directory.Create(name="root", website=self.website)
        dir1 = Directory.Create(name="Something", website=self.website)
        dir2 = Directory.Create(name="Something2", website=self.website)
        dir3 = Directory.Create(name="Something", website=self.website)

        root.addChild(dir1)
        root.addChild(dir2)
        dir2.addChild(dir3)

        self.assertEqual(len(root.children), 2)
        self.assertEqual(len(dir1.children), 0)
        self.assertEqual(len(dir2.children), 1)
        self.assertEqual(len(dir3.children), 0)

        for i in root.children:
            self.assertEqual(type(i), Directory)
            pass
        for i in dir2.children:
            self.assertEqual(type(i), Directory)
            pass

        ##Test if addDir works
        dir3.addChildDir(name="Things", website=self.website)
        dir3.addChildDir(name="Things2", website=self.website)
        dir3.addChildDir(name="Things4", website=self.website)

        self.assertEqual(len(dir3.children), 3)

        self.assertRaises(IntegrityError, dir3.addChildDir, name="Things", website=self.website)
        self.assertRaises(IntegrityError, dir2.addChildDir, name="Something", website=self.website)
        self.assertRaises(IntegrityError, dir2.addChild, dir3)
        pass

    def test_render(self):
        root = Directory.Create(name="root", website=self.website)
        dir1 = Directory.Create(name="Something", website=self.website)
        dir2 = Directory.Create(name="Something2", website=self.website)
        dir3 = Directory.Create(name="Something", website=self.website)

        root.addChild(dir1)
        root.addChild(dir2)
        dir2.addChild(dir3)

        actualMap = {
            "id": root.id,
            "name": root.name,
            "type": "dir",
            "sys_name": root.sys_name,
            "children": [
                {
                    "id": dir1.id,
                    "name": dir1.name,
                    "type": "dir",
                    "sys_name": dir1.sys_name,
                    "children": []
                },
                {
                    "id": dir2.id,
                    "name": dir2.name,
                    "type": "dir",
                    "sys_name": dir2.sys_name,
                    "children": [
                        {
                            "id": dir3.id,
                            "name": dir3.name,
                            "type": "dir",
                            "sys_name": dir3.sys_name,
                            "children": []
                        },
                    ]
                },
            ]
        }

        self.assertEqual(root.render(), actualMap)
        pass
