from flask_wtf import Form
import wtforms

class ResellerSettings(Form):
    name = wtforms.StringField('Change your business name')
    directory = wtforms.StringField('Change the shuttl directory')
    price = wtforms.FloatField("Set your pricing")

    def __init__(self, reseller, *args, **kwargs):
        self.name.default = reseller.name
        self.directory.default = reseller.subdir
        self.price.default = reseller.price
        self.process()
        super(ResellerSettings, self).__init__(*args, **kwargs)
        pass

    def save(self, reseller):
        reseller.name = self.name.data
        reseller.subdir = self.directory.data
        reseller.price = self.price.data
        reseller.save()
        pass
    pass