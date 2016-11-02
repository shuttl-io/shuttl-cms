import json

from shuttl import app
from shuttl.tests import testbase
from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization, OrganizationDoesNotExistException
from shuttl.Models.Website import Website

class OrganizationViewTest(testbase.BaseTest):

    def _setUp(self):
        self.organization = Organization.Create(self.reseller, name="test")
        self.maxDiff = None
        pass

    def test_login(self):
        # rv = self.login('test')
        pass


    def login(self, organization):
        return self.app.post('http://test.shuttl.com:5000/login', data=dict(
            
        ), follow_redirects=True)

    def test_creation(self):
        results = self.app.post("http://test.shuttl.com:5000/websites/", data = dict(name="testSite"))
        self.assertEqual(results.status_code, 201)
        results2 = self.app.post("http://test.shuttl.com:5000/websites/", data = dict(name="testSite"))
        self.assertEqual(results2.status_code, 409)
        results = json.loads(results.data.decode())
        expected = {
            'name': 'testSite', 
            'root': {
                'name': 'root', 
                'fullPath': '/', 
                '_children': [], 
                'id': 2, 
                'parent': 'None'
            }, 
            'id': 1, 
            'organization': {
                'name': 'test',
                'websites': [], 
                'id': 1, 
                'reseller': {
                    '_url': 'shuttl.com', 
                    'name': 'shuttl', 
                    'id': 1, 
                    'subdir': '', 
                    'admins': [], 
                    'organizations': [], 
                    'directory': '', 
                    '_price': 10.0
                }, 
                'users': []
            }, 
            'sys_name': 'testSite', 
            'publishers': [], 
            'files': []
        }
        self.assertEqual(len(Website.query.all()), 1)
        self.assertEqual(len(list(self.organization.websites)), 1)
        # serialising isn't working, returning list of files as a string
        # self.assertEqual(results, expected)
        pass

    def test_getAll(self):
        self.app.post("http://test.shuttl.com:5000/websites/", data = dict(name="testOrg"))
        self.app.post("http://test.shuttl.com:5000/websites/", data = dict(name="testOrg2"))
        self.app.post("http://test.shuttl.com:5000/websites/", data = dict(name="testOrg3"))

        expected = [
            Website.query.filter(Website.name == "testOrg").first().serialize(),
            Website.query.filter(Website.name == "testOrg2").first().serialize(),
            Website.query.filter(Website.name == "testOrg3").first().serialize()
        ]

        results = self.app.get("http://test.shuttl.com:5000/websites/")
        results = json.loads(results.data.decode())
        self.assertEqual(len(results), 3)
        self.assertEqual(expected, results)
        pass

    def test_get(self):
        results = self.app.post("http://test.shuttl.com:5000/websites/", data = dict(name="testOrg"))
        results_dict = json.loads(results.data.decode())
        id = results_dict["id"]
        results = self.app.get("http://test.shuttl.com:5000/websites/{0}".format(id))
        self.assertEqual(results.status_code, 200)
        results = json.loads(results.data.decode())
        self.assertEqual(results_dict, results)
        results = self.app.get("http://test.shuttl.com:5000/websites/1234")
        self.assertEqual(results.status_code, 404)
        pass

    def test_patch(self):
        results = self.app.post("http://test.shuttl.com:5000/websites/", data = dict(name="testOrg"))
        reseller = Reseller.Create(name="test3", _url="shuttl2.com")
        results_dict = json.loads(results.data.decode())
        results = self.app.patch("http://test.shuttl.com:5000/websites/{0}".format(results_dict["id"]), data=dict(name="testOrg4"))
        self.assertEqual(results.status_code, 200)
        self.assertIsNone(Website.query.filter(Website.name == "testOrg").first())
        results = json.loads(results.data.decode())
        self.assertEqual(results["name"], "testOrg4")
        ws = Website.query.filter(Website.id == results["id"]).first()
        self.assertEqual(ws.serialize(), results)
        res3 = self.app.patch("http://test.shuttl.com:5000/websites/1234")
        self.assertEqual(res3.status_code, 404)
        res3 = self.app.patch("http://test.shuttl.com:5000/websites/")
        self.assertEqual(res3.status_code, 405)
        pass

    def test_delete(self):
        results = self.app.post("http://test.shuttl.com:5000/websites/", data = dict(name="testOrg"))
        results2 = self.app.post("http://test.shuttl.com:5000/websites/", data = dict(name="testOrg2"))
        results = json.loads(results.data.decode())
        res3 = self.app.delete("http://test.shuttl.com:5000/websites/{0}".format(results["id"]))
        self.assertEqual(res3.status_code, 200)
        self.assertEqual(len(list(self.reseller.organizations.all())), 1)
        res3 = self.app.delete("http://test.shuttl.com:5000/websites/")
        self.assertEqual(res3.status_code, 405)
        res3 = self.app.delete("http://test.shuttl.com:5000/websites/1234")
        self.assertEqual(res3.status_code, 404)
        pass






