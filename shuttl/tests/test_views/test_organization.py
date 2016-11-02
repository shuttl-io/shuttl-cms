import json

from shuttl import app
from shuttl.tests import testbase
from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization, OrganizationDoesNotExistException

class OrganizationViewTest(testbase.BaseTest):
    def _setUp(self):
        pass

    def test_index(self):
        # rv = self.app.get('/')
        # assert 'Shuttl' in rv.data.decode('utf-8')
        pass

    def test_login(self):
        rv = self.login('test')
        pass


    def login(self, organization):
        return self.app.post('/login', data=dict(
            organization=organization
        ), follow_redirects=True)

    def test_creation(self):
        results = self.app.post("/organization/", data = dict(name="testOrg"))
        self.assertEqual(results.status_code, 201)
        results2 = self.app.post("/organization/", data = dict(name="testOrg"))
        self.assertEqual(results2.status_code, 409)
        results = json.loads(results.data.decode())
        expected = {
            'reseller': {
                'directory': '',
                'name': 'shuttl',
                '_url': 'shuttl.com',
                'subdir': '',
                'id': 1,
                'admins': [],
                'organizations': [],
                '_price': 10.0
            },
            'id': 1,
            'name': 'testOrg',
            'websites': [],
            'users': []
        }
        self.assertEqual(len(Organization.query.all()), 1)
        self.assertEqual(len(list(self.reseller.organizations.all())), 1)
        self.assertEqual(results, expected)
        pass

    def test_getAll(self):
        self.app.post("/organization/", data = dict(name="testOrg"))
        self.app.post("/organization/", data = dict(name="testOrg2"))
        self.app.post("/organization/", data = dict(name="testOrg3"))

        expected = [
            Organization.query.filter(Organization.name == "testOrg").first().serialize(),
            Organization.query.filter(Organization.name == "testOrg2").first().serialize(),
            Organization.query.filter(Organization.name == "testOrg3").first().serialize()
        ]

        results = self.app.get("/organization/")
        results = json.loads(results.data.decode())
        self.assertEqual(len(results), 3)
        self.assertEqual(expected, results)
        pass

    def test_get(self):
        results = self.app.post("/organization/", data = dict(name="testOrg"))
        results_dict = json.loads(results.data.decode())
        id = results_dict["id"]
        results = self.app.get("/organization/{0}".format(id))
        self.assertEqual(results.status_code, 200)
        results = json.loads(results.data.decode())
        self.assertEqual(results_dict, results)
        results = self.app.get("/organization/1234")
        self.assertEqual(results.status_code, 404)
        pass

    def test_patch(self):
        results = self.app.post("/organization/", data = dict(name="testOrg"))
        reseller = Reseller.Create(name="test3", _url="shuttl2.com")
        results_dict = json.loads(results.data.decode())
        results = self.app.patch("/organization/{0}".format(results_dict["id"]), data=dict(name="testOrg4"))
        self.assertEqual(results.status_code, 200)
        self.assertRaises(OrganizationDoesNotExistException, Organization.Get, name="testOrg", vendor=self.reseller)
        results = json.loads(results.data.decode())
        self.assertEqual(results["name"], "testOrg4")
        org = Organization.Get(name="testOrg4", vendor=self.reseller)
        self.assertEqual(org.serialize(), results)
        results = self.app.patch("/organization/{0}".format(results_dict["id"]), data=dict(vendor=reseller.id))
        self.assertRaises(OrganizationDoesNotExistException, Organization.Get, name="testOrg4", vendor=self.reseller)
        results = json.loads(results.data.decode())
        org = Organization.Get(name="testOrg4", vendor=reseller)
        self.assertEqual(org.serialize(), results)
        self.assertEqual(len(list(self.reseller.organizations.all())), 0)
        self.assertEqual(len(list(reseller.organizations.all())), 1)
        results = self.app.patch("/organization/1234", data=dict(vendor=reseller.id))
        self.assertEqual(results.status_code, 404)
        results = self.app.patch("/organization/", data=dict(vendor=reseller.id))
        self.assertEqual(results.status_code, 405)
        pass

    def test_delete(self):
        results = self.app.post("/organization/", data = dict(name="testOrg"))
        results2 = self.app.post("/organization/", data = dict(name="testOrg2"))
        results = json.loads(results.data.decode())
        res3 = self.app.delete("/organization/{0}".format(results["id"]))
        self.assertEqual(res3.status_code, 200)
        self.assertEqual(len(list(self.reseller.organizations.all())), 1)
        res3 = self.app.delete("/organization/")
        self.assertEqual(res3.status_code, 405)
        res3 = self.app.delete("/organization/1234")
        self.assertEqual(res3.status_code, 404)
        pass






