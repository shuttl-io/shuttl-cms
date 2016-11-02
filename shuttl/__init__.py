import sys
from flask import Flask, redirect, request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_wtf.csrf import CsrfProtect

from .sessions import ShuttlSessionInterface

app = Flask(__name__)
app.config.from_object("shuttl.settings.DevelopmentConfig")
app.session_interface = ShuttlSessionInterface()
csrf = CsrfProtect(app)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from shuttl.MiddleWare import OrganizationMiddleware
from .Views import *
from .Models import *
from .misc import shuttl, shuttlOrgs

@login_manager.unauthorized_handler
def unauthorized():
    url = redirect(url_for("shuttlOrgs.login", organization=request.organization.sys_name))
    return url


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


from .Commands.FillDB import FillDB
from .Commands.TestSuite import TestSuite
from .Commands.DemoFiller import DemoFiller
from .Commands.ResetPublishers import ResetPublishers
from .Commands.UploadToS3 import UploadS3
from .Templates.Tags import load_tags

# load_tags(app.jinja_env)

manager.add_command('test', TestSuite())

manager.add_command('filldb', FillDB())

manager.add_command('demofiller', DemoFiller())
manager.add_command("resetQueue", ResetPublishers())

manager.add_command('upload', UploadS3)

app.register_blueprint(shuttl)
app.register_blueprint(shuttlOrgs)

from .Models.Reseller import Reseller, ResellerDoesNotExist
from .Models.organization import Organization, OrganizationDoesNotExistException

@app.before_request
def before_request():
    request.organization = None
    # hostname = request.headers.get("host")
    # try:
    #     reseller = Reseller.GetNameFromHost(hostname)
    #     try:
    #         hostname = request.headers.get("host").split("//", 1)[-1]
    #         subdomain = hostname.split(".", 1)[0]
    #         request.organization = Organization.Get(name=subdomain.replace("_", " "), vendor = reseller)
    #     except OrganizationDoesNotExistException:
    #         pass
    #     pass
    # except ResellerDoesNotExist:
    #     pass
    pass

@app.teardown_request
def teardown_request(exception):
    pass

from .Models.FileTree.FileObjects.FileObject import FileObject
FileObject.LoadMapper()

@app.before_first_request
def beforeFirstRequest():
    from .Templates.Tags import load_tags
    load_tags(app.jinja_env)
