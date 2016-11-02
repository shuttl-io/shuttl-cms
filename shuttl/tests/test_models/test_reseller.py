from shuttl.tests import testbase

from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization
from shuttl.Models.User import User

class ResellerTestCase(testbase.BaseTest):

    def test_create(self):
        reseller = Reseller.Create(name="things", url="things.com")
        reseller = Reseller.query.get(reseller.id)
        self.assertEqual(reseller.name, "things")
        self.assertEqual(reseller._url, "things.com")
        self.assertEqual(reseller.url, "http://things.com/")
        self.assertEqual([], reseller.organizations.all())
        self.assertEqual(list(reseller.admins), [])
        reseller.name = "test"
        reseller.save()
        reseller = Reseller.query.get(reseller.id)
        self.assertNotEqual(reseller.name, "things")
        self.assertEqual(reseller.name, "test")
        pass

    def test_organization(self):
        reseller = Reseller.Create(name="things", url="things.com")
        reseller2 = Reseller.Create(name="things2", url="things2.com")
        org = Organization.Create(name="test_org", reseller=reseller)
        self.assertEqual(org.id, reseller.organizations[0].id)
        self.assertEqual([], reseller2.organizations.all())
        org.setReseller(reseller2)
        self.assertEqual(org.id, reseller2.organizations[0].id)
        self.assertEqual([], reseller.organizations.all())
        pass

    def test_admin(self):
        reseller = Reseller.Create(name="things", url="things.com")
        user = User.Create(organization=None, username="Tester", email="Test@tesi.com", password="Things", reseller=reseller)
        reseller = Reseller.query.get(reseller.id)
        user = User.query.get(user.id)
        self.assertTrue(user in reseller.admins)
        self.assertEqual(user.reseller, reseller)
        pass

    def test_hostname(self):
        reseller = Reseller.Create(name="things", url="things.com")
        reseller2 = Reseller.GetFromHostname("things.com")
        self.assertEqual(reseller, reseller2)
        pass

    def test_contacts(self):
        reseller = Reseller.Create(name="things", url="things.com")
        user = User.Create(organization=None, username="Tester", email="Test@tesi.com", password="Things", reseller=reseller)
        user.isContact = True
        user.save()
        user2 = User.Create(organization=None, username="Tester", email="Test@tesi.com", password="Things", reseller=reseller)
        user2.isContact = True
        user2.save()
        user3 = User.Create(organization=None, username="Tester", email="Test@tesi.com", password="Things", reseller=reseller)
        self.assertTrue(user in reseller.contacts)
        self.assertTrue(user in reseller.admins)
        self.assertTrue(user2 in reseller.contacts)
        self.assertTrue(user2 in reseller.admins)
        self.assertFalse(user3 in reseller.contacts)
        self.assertTrue(user3 in reseller.admins)
        pass