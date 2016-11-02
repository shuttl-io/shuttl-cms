from unittest import mock

from shuttl.Models.User import User
from shuttl.Forms.OrganizationSignupForm import OrganizationSignupForm
import shuttl.Views.organization as view
from shuttl.Models.organization import Organization
from shuttl.tests import testbase


class OrganizationSignupTest(testbase.BaseTest):
    def _setUp(self):
        self.organization = Organization.Create(self.reseller, name="test")
        pass

    @mock.patch('shuttl.Models.User.emailUser')
    def test_signup(self, mocked_send):
        from shuttl import csrf
        signup = csrf.exempt(view.signup)
        result = self.app.post(
            'http://test.shuttl.com:5000/signup',
            data=dict(
                firstname='Nico',
                lastname='Vergara',
                username="vegara",
                email='me@nicovergara.io',
                password='password'
            )
        )
        result2 = self.app.post(
            'http://test.shuttl.com:5000/signup',
            data=dict(
                firstname='Nico',
                lastname='Vergara',
                username="nico_vegara",
                email='nico@shuttl.io',
                password='password'
            )
        )
        result3 = self.app.post(
            'http://test.shuttl.com:5000/signup',
            data=dict(
                firstname='Bob',
                lastname='Smith',
                username='nico',
                email='me@nicovergara.io',
                password='password'
            )
        )

        result4 = self.app.post(
            'http://test.shuttl.com:5000/signup',
            data=dict(
                firstname='Bob',
                lastname='Smith',
                username='vegara',
                email='me2@nicovergara.io',
                password='password'
            )
        )
        user = User.query.all()
        self.assertEquals(result.status_code, 302)
        self.assertEquals(result.headers.get('location'), 'http://test.shuttl.com:5000/confirm/me%40nicovergara.io')
        self.assertEquals(result2.status_code, 302)
        self.assertEquals(result2.headers.get('location'), 'http://test.shuttl.com:5000/confirm/nico%40shuttl.io')
        self.assertEquals(result3.status_code, 302)
        self.assertEquals(result3.headers.get('location'), 'http://test.shuttl.com:5000/signup?error=-2')
        self.assertEquals(result4.status_code, 302)
        self.assertEquals(result4.headers.get('location'), 'http://test.shuttl.com:5000/signup?error=-1')
        self.assertEquals(len(user), 2)
        self.assertEquals(user[0].username, 'vegara')
        pass

    pass
