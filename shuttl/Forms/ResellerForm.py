from flask_wtf import Form, RecaptchaField
import wtforms
from wtforms.validators import DataRequired, url
from wtforms.fields.html5 import URLField

from .UserForm import BaseUserForm
from shuttl.Models.Reseller import Reseller

class ResellerForm(BaseUserForm):
    name = wtforms.StringField('Your business name', validators=[DataRequired()])
    url = URLField("The url for your business", validators=[DataRequired(), url()])
    directory = wtforms.StringField('Subdirectory to host shuttl on')
    # recaptcha = RecaptchaField()

    def save(self, commit=True):
        url = self.url.data
        url = url.split("/", 2)[-1]
        url = url.split("/")[0]
        reseller = Reseller(name=self.name.data, url=url, subdir=self.directory.data)
        if commit:
            reseller.save()
        user = super(ResellerForm, self).save(False)
        user.reseller = reseller
        user.save()
        user.verify()
        return reseller

    pass