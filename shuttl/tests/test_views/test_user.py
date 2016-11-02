import json

from shuttl import app
from shuttl.tests import testbase
from shuttl.Models import User
from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization, OrganizationDoesNotExistException

class UserViewTest(testbase.BaseTest):
    def _setUp(self):
        self.organization = Organization.Create(name="test", reseller=self.reseller)
        pass

    # def test_index(self):
    #     # rv = self.app.get('/')
    #     # assert 'Shuttl' in rv.data.decode('utf-8')
    #     pass

    def test_login(self):
        rv = self.login('test')
        pass

    def login(self, organization):
        return self.app.post('/login', data=dict(
            organization=organization
        ), follow_redirects=True)

    def test_creation(self):
        response = self.app.post("http://test.shuttl.com:5000/user", \
                                 data=dict(organization=self.organization.id, username="test", email="test@test.com", \
                                            password="test", reseller=self.reseller.id))
        self.assertEqual(response.status_code, 201)
        response2 = self.app.post("http://test.shuttl.com:5000/user", data=dict(organization=self.organization.id, username="test", email="test@test.com", password="test", reseller=self.reseller.id))
        self.assertEqual(response2.status_code, 409)
        results = json.loads(response.data.decode())


        ###### SERIALIZE NEEDS TO BE MODIFIED TO HANDLE list of objects, e.g. an organization #########
        pass

    def test_getAll(self):
        self.app.post("http://test.shuttl.com:5000/user", \
                                 data=dict(organization=self.organization.id, username="test", email="test@test.com", \
                                           password="test", reseller=self.reseller.id))
        self.app.post("http://test.shuttl.com:5000/user", \
                                 data=dict(organization=self.organization.id, username="test2", email="test2@test.com", \
                                           password="test", reseller=self.reseller.id))
        self.app.post("http://test.shuttl.com:5000/user", \
                                 data=dict(organization=self.organization.id, username="test3", email="test3@test.com", \
                                           password="test", reseller=self.reseller.id))
        expected = [
            User.query.filter(User.username == "test").first().serialize(),
            User.query.filter(User.username == "test2").first().serialize(),
            User.query.filter(User.username == "test3").first().serialize()
        ]

        results = self.app.get("http://test.shuttl.com:5000/user")
        results = json.loads(results.data.decode())
        self.assertEqual(len(results), 3)
        self.assertEqual(expected, results)
        pass

    def test_get(self):
        results = self.app.post("http://test.shuttl.com:5000/user", \
                                 data=dict(organization=self.organization.id, username="test", email="test@test.com", \
                                           password="test", reseller=self.reseller.id))
        results_dict = json.loads(results.data.decode())
        id = results_dict["id"]

        results = self.app.get("http://test.shuttl.com:5000/user/{0}".format(id))
        self.assertEqual(results.status_code, 200)

        results = json.loads(results.data.decode())
        self.assertEqual(results_dict, results)

        results = self.app.get("http://test.shuttl.com:5000/user/1234")
        self.assertEqual(results.status_code, 404)
        pass

    def test_patch(self):
        results = self.app.post("http://test.shuttl.com:5000/user", \
                                data=dict(organization=self.organization.id, username="test", email="test@test.com", \
                                          password="test", reseller=self.reseller.id))
        organization = Organization.Create(name="test2", reseller=self.reseller)
        results_dict = json.loads(results.data.decode())
        results = self.app.patch("http://test.shuttl.com:5000/user/{0}".format(results_dict["id"]), \
                                 data=dict(organization=self.organization.id, username="test_update", firstName="Gabe", \
                                           lastName="Morcote", email="test@test.com", password="test", isAdmin=0, reseller=self.reseller.id))
        self.assertEqual(results.status_code, 200)
        self.assertEqual(None, User.query.filter(User.username=="test").first())

        results_dict = json.loads(results.data.decode())
        self.assertEqual(results_dict["username"], "test_update")
        user = User.query.filter(User.username=="test_update").first()
        self.assertEqual(user.serialize(), results_dict)

        results = self.app.patch("http://test.shuttl.com:5000/user/{0}".format(results_dict["id"]), \
                                 data=dict(organization=organization.id, username="test_update", firstName="Gabe", \
                                           lastName="Morcote", email="test@test.com", password="test", isAdmin=0,
                                           reseller=self.reseller.id))
        self.assertEqual(results.status_code, 200)
        user = User.query.filter(User.organization==organization).first()
        self.assertIsNotNone(user)
        pass

    def test_delete(self):
        results = self.app.post("http://test.shuttl.com:5000/user", \
                                 data=dict(organization=self.organization.id, username="test", email="test@test.com", \
                                           password="test", reseller=self.reseller.id))
        results2 = self.app.post("http://test.shuttl.com:5000/user", \
                                 data=dict(organization=self.organization.id, username="test2", email="test2@test.com", \
                                           password="test", reseller=self.reseller.id))

        results = json.loads(results.data.decode())
        result3 = self.app.delete("http://test.shuttl.com:5000/user/{0}".format(results["id"]))

        self.assertEqual(result3.status_code, 200)
        self.assertEqual(len(list(self.reseller.organizations.all())), 1)

        result3 = self.app.delete("http://test.shuttl.com:5000/user")
        self.assertEqual(result3.status_code, 405)

        result3 = self.app.delete("http://test.shuttl.com:5000/user/1234")
        self.assertEqual(result3.status_code, 404)
        pass






