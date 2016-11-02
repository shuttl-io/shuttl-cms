##
# @file misc.py
from flask import Blueprint
from urllib.parse import urlparse
#from shuttl.Models.organization import Organization

shuttl = Blueprint('shuttl', __name__,
                        template_folder='static/templates')

shuttlOrgs = Blueprint('shuttlOrgs', __name__,
                        template_folder='static/templates',
                        subdomain="<organization>"
                       )

##To be returned so that attrs can be referenced even if they don't exist
class AttrClass:
    def __init__(self, retStr=""):
        self.retStr = retStr
        pass

    def __getattr__(self, attr):
        return self

    def __str__(self):
        return self.retStr

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        return self

    def __iter__(self):
        return iter([])
    pass

##To be returned so that attrs can be referenced even if they don't exist
class ContentAttr:
    def __init__(self, webpage):
        self.webpage = webpage
        pass

    def __getattr__(self, attr):
        try:
            return self.webpage[attr]
        except KeyError:
            return AttrClass()
        pass

    def __str__(self):
        return str(self.webpage)

    def __repr__(self):
        return str(self)