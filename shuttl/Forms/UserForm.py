from flask_wtf import Form
import wtforms
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField

from shuttl.Models.User import User

class BaseUserForm(Form):
    username = wtforms.StringField("Your Username", validators=[DataRequired()], render_kw={"placeholder": "Username"})
    firstname = wtforms.StringField('Your first name', validators=[DataRequired()], render_kw={"placeholder": "First name"})
    lastname = wtforms.StringField('Your last name', validators=[DataRequired()], render_kw={"placeholder": "Last name"})
    email = EmailField("Your Email Address", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = wtforms.PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})

    def save(self, commit=True):
        username = self.username.data
        email = self.email.data
        user = User(username=username, email=email)
        user.firstName = self.firstname.data
        user.lastName = self.lastname.data
        user.setPassword(self.password.data)
        if commit:
            user.save()
            pass
        return user

    pass
