from flask_wtf import Form
import wtforms
from wtforms.validators import DataRequired
from shuttl.Models.organization import Organization


class LoginForm(Form):
    email = wtforms.StringField("email", validators=[DataRequired()], render_kw={"placeholder": "Email"})
    password = wtforms.PasswordField("password", validators=[DataRequired()], render_kw={"placeholder": "Password"})

    ## Loads a user from an organization
    # \param organization the organization that will be tied to the request
    # \return a user that belongs to that organization
    def loadUser(self, organization):
        return organization.GetUser(email=self.email.data, password=self.password.data)
    pass
