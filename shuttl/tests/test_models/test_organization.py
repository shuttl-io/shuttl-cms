from shuttl.tests import testbase
from shuttl.Models.organization import Organization, OrganizationDoesNotExistException
from shuttl.Models.User import User
from shuttl.Models.Reseller import Reseller
from sqlalchemy.exc import IntegrityError

class OrganizationTestCase(testbase.BaseTest):

    def _setUp(self):
        self.reseller = Reseller.Create(name="test", url="test4.com")
        pass

    def test_create(self):
        organization = Organization("Test", reseller=self.reseller)
        organization.save()
        org2 = Organization.query.filter_by(name="Test").first()
        self.assertEqual(org2, organization)
        org3 = Organization("Test", reseller=self.reseller)
        self.assertRaises(IntegrityError, org3.save)
        org3 = Organization("Test2", reseller=self.reseller)
        org3.save()
        count = Organization.query.filter_by(name="Test2").count()
        self.assertEqual(count, 1)
        pass

    def test_get(self):
        org2 = Organization.Create(name="Thing", reseller=self.reseller)
        org = Organization.Get(name="Thing", vendor=self.reseller)
        self.assertEqual(org, org2)
        self.assertRaises(OrganizationDoesNotExistException, Organization.Get, name="blah", vendor=self.reseller)
        pass

    def test_contains(self):
        org = Organization.Create(name="Thing", reseller=self.reseller)
        org2 = Organization.Create(name="Thing2", reseller=self.reseller)
        usr = User(username="thing", email="Blah")
        usr.setPassword("Things")
        usr.organization = org
        usr.save()
        usr2 = User(username="thing", email="Blah")
        usr2.setPassword("Things")
        usr2.isFree = True
        usr2.save()

        self.assertTrue(org.containsUser(username="thing", email="Blah"))
        self.assertFalse(org.containsUser(username="thing2", email="Blah2"))
        self.assertTrue(org.containsUser(username="thing", email="Blah2"))
        self.assertTrue(org.containsUser(username="thing2", email="Blah"))

        self.assertFalse(org2.containsUser(username="thing", email="Blah"))
        self.assertFalse(org2.containsUser(username="thing2", email="Blah2"))
        self.assertFalse(org2.containsUser(username="thing", email="Blah2"))
        self.assertFalse(org2.containsUser(username="thing2", email="Blah"))

        self.assertTrue(org.containsUser(user=usr))
        self.assertFalse(org.containsUser(user=usr2))
        self.assertFalse(org2.containsUser(user=usr))
        pass
