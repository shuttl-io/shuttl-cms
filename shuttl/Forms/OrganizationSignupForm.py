from flask_wtf import Form, RecaptchaField
import wtforms
from wtforms.validators import DataRequired, url
from wtforms.fields.html5 import URLField

from .UserForm import BaseUserForm
from shuttl.Models.User import User


class OrganizationSignupForm(BaseUserForm):
    organization = None      #pass this in from the view function

    def save(self, commit=True):
        username = self.username.data
        email = self.email.data
        user = User.Create(username=username, email=email, organization=self.organization)
        user.firstName = self.firstname.data
        user.lastName = self.lastname.data
        user.setPassword(self.password.data)
        if commit:
            user.save()
            pass
        user.save()
        user.sendVerifyMessage()
        return user

    pass
