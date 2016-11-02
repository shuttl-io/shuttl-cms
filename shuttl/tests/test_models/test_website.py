import unittest

from shuttl import app
from shuttl.tests import testbase
from shuttl.Models.Website import Website
from shuttl.Models.FileTree.Directory import Directory
from shuttl.Models.organization import Organization
from sqlalchemy.exc import IntegrityError
from shuttl.Models.Reseller import Reseller


class WebsiteTestCase(testbase.BaseTest):

    def _setUp(self):
        self.reseller = Reseller(name="test4", url="test2.com")
        self.reseller.save()
        self.organization = Organization.Create(name="TestOrg", reseller=self.reseller)
        self.website = Website.Create(name="Thing", organization=self.organization)
        pass

    def test_create(self):
        website2 = Website.query.get(self.website.id)
        self.assertEqual(self.website, website2)
        self.assertEqual(website2.name, "Thing")
        self.assertEqual(website2.organization, self.organization)
        self.assertEqual(website2.sys_name, "Thing")
        self.assertIsNotNone(website2.organization_id)

        self.assertRaises(IntegrityError, Website.Create, name="Thing", organization=self.organization)

        website = Website.Create(name="Thing thing", organization=self.organization)
        website3 = Website.query.get(website.id)
        self.assertEqual(website3.sys_name, "Thing_thing")
        self.assertIsNotNone(website3.organization_id)
        self.assertTrue(website2 in self.organization.websites)
        self.assertTrue(website3 in self.organization.websites)
        pass

    def test_rootCreation(self):
        organization = Organization.Create(name="TestOrg2", reseller=self.reseller)
        website = Website.Create(name="Thing", organization=organization)
        self.assertIsNotNone(website.root)
        dir = website.root
        website2 = Website.query.get(website.id)

        website = Website.Create(name="Thing2", organization=organization)

        self.assertEqual(dir, website2.root)
        self.assertNotEqual(website.root, website2.root)
        pass

    @unittest.skipIf(app.config["SHOULD_SKIP"], reason='fix later')
    def test_render(self):
        root = self.website.root

        dir1 = Directory.Create(name="Something", website=self.website)
        dir2 = Directory.Create(name="Something2", website=self.website)
        dir3 = Directory.Create(name="Something", website=self.website)

        root.addChild(dir1)
        root.addChild(dir2)
        dir2.addChild(dir3)

        actualMap = {
            "children": [
                {
                    "children": [],
                    "id": 4,
                    "name": "Something",
                    "sys_name": "Something",
                    "type": "dir"
                },
                {
                    "children": [
                        {
                            "children": [],
                            "id": 6,
                            "name": "Something",
                            "sys_name": "Something",
                            "type": "dir"
                        }
                    ],
                    "id": 5,
                    "name": "Something2",
                    "sys_name": "Something2",
                    "type": "dir"
                },
                {
                    "children": [],
                    "id": 3,
                    "name": "_hidden",
                    "sys_name": "_hidden",
                    "type": "dir"
                }
            ],
            "id": 2,
            "name": "root",
            "sys_name": "root",
            "type": "dir"
        }

        renderRes = self.website.render()
        self.assertEqual(renderRes, actualMap)
        pass
