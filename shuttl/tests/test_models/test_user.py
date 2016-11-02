from shuttl.tests import testbase

from shuttl.Models.User import User, UserDataTakenException, NoOrganizationException, ToManyOrganizations
from shuttl.Models.organization import Organization
from shuttl.Models.Reseller import Reseller

class UserTestCase(testbase.BaseTest):

    def _setUp(self):
        self.reseller = Reseller(name ="test4", url="test2.com")
        self.reseller.save()
        pass

    def test_create(self):
        organization = Organization(name="Test", reseller=self.reseller)
        organization.save()
        organization = Organization.Get(name="Test", vendor=self.reseller)
        data = dict(organization=organization, username="Tester", email="Test@tesi.com", password="Things")
        user = User.Create(**data)
        self.assertRaises(UserDataTakenException, User.Create, **data)
        user2 = User.query.get(user.id)
        self.assertEqual(user2.username, user.username)
        self.assertEqual(user2, user)
        self.assertEqual(user2.password, user.password)
        self.assertNotEqual(user2.password, "Things")
        self.assertFalse(user.isAdmin)
        self.assertFalse(user.isFree)
        self.assertFalse(user.isActive)
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_active)
        self.assertIsNotNone(user2.organization)
        user.organization = None
        self.assertRaises(NoOrganizationException, user.save)
        
        pass

    def test_password(self):
        org = Organization.Create(name="Test", reseller=self.reseller)
        usr = User.Create(organization=org, username="Tester", email="blah@blah.com", password="Bullshit")
        oldPW = usr.password
        self.assertNotEqual(usr.password, "Bullshit")
        self.assertTrue(usr.checkPassword("Bullshit"))
        usr.setPassword("Things")
        self.assertNotEqual(usr.password, oldPW)
        self.assertTrue(usr.checkPassword("Things"))
        pass
