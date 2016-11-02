from shuttl.tests import testbase
from shuttl.Models.organization import Organization
from shuttl.MiddleWare.OrganizationMiddleware import organization_required
from werkzeug.exceptions import NotFound

@organization_required
def testmock():
    return True


@organization_required
def testmock2(arg1):
    return True

class OrganizationMiddlewareTestCase(testbase.BaseTest):

    def _setUp(self):
        self.org = Organization.Create(name='test', reseller=self.reseller)
        self.org2 = Organization.Create(name='testing', reseller=self.reseller)
        pass

    def test_organization(self):
        self.assertTrue(testmock(self.org.name))
        self.assertTrue(testmock(self.org2.name))
        self.assertTrue(testmock('test'))
        self.assertTrue(testmock2('test', False))
        self.assertRaises(NotFound, testmock, 'stuff')
        pass
