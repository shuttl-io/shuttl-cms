from shuttl.Models.Reseller import Reseller
from flask import render_template, redirect, url_for, request, jsonify, abort, Response, send_from_directory
from flask.ext.login import login_user
import json

from shuttl import csrf, app
from shuttl.MiddleWare.OrganizationMiddleware import reseller_required, reseller_login, organization_required
from shuttl.misc import shuttl, shuttlOrgs
from shuttl.Models.Validators.Reseller import ResellerValidator
from shuttl.Models.organization import Organization, OrganizationExists
from shuttl.Models import User
from shuttl.Models.User import UserDataTakenException
from shuttl.Forms.ResellerForm import ResellerForm
from shuttl.Forms.LoginForm import LoginForm
from shuttl.Forms.ResellerSettingsForm import ResellerSettings
from shuttl.Models.FileTree.FileObjects.FileObject import FileObject

# @shuttl.route('/signup', methods=["GET", "POST"])
# def createReseller():
#     form = ResellerForm()
#     if form.validate_on_submit():
#         reseller = form.save()
#         return redirect(url_for("shuttl.nextSteps", reseller=reseller.id))
#     return render_template('reseller.html', form=form)
#
# @shuttl.route("/<reseller>/nextsteps")
# def nextSteps(reseller):
#     reseller = Reseller.query.get(reseller)
#     return render_template("next_steps.html", reseller=reseller)

# @shuttl.route("/login", methods=["GET", "POST"])
# @reseller_required
# def login():
#     error = request.form.get("e")
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = form.loadUser(request.reseller)
#         if user is None:
#             return redirect("/login?e=1")
#         login_user(user, remember=True)
#         return redirect(url_for("shuttl.dashboard"))
#     return render_template("vendors/login.html", error=error, form=form)

# @shuttl.route("/validate/<string:token>", methods=["POST", "GET"])
# @reseller_required
# def validate(token):
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = form.loadUser(request.reseller)
#         if user is None:
#             return redirect(url_for("shuttl.validate", token=token))
#         ResellerValidator.Validate(token=token, user=user)
#         login_user(user, remember=True)
#         return redirect(url_for("shuttl.dashboard"))
#     return render_template("vendors/validate.html", vendor=request.reseller, token=token, form=form)

# @shuttl.route("/dashboard")
# @reseller_login
# def dashboard():
#     return render_template("vendors/dashboard.html", reseller=request.reseller, )
#
# @shuttl.route("/settings", methods=["POST", "GET"])
# @reseller_login
# def settings():
#     form = ResellerSettings(request.reseller)
#     if form.validate_on_submit():
#         form.save(request.reseller)
#         return redirect(url_for("shuttl.setings"))
#     return render_template("vendor/settings.html", vendor=request.reseller, form=form)

# TODO: make this login required.
## This is an api endpoint for the vendors to modify the organizations
# \method{GET, POST, PATCH, DELETE}
# \url /organization/:organization_id
# \url /organization
# \param name needed for creating. optional for updating. not needed for deleting or getting
# \param vendor optional, the id of a vendor used to transfer an organization to a new vendor
# \param :organization_ the id of the organization. needed for deleting, updating, and Getting a singlular organization
# if not included for a Get request, this will get all organizations associated with a vendor.
@csrf.exempt
@shuttl.route("/organization/", defaults={"organization": None}, methods=["POST", "GET"])
@shuttl.route("/organization/<organization>", methods=["POST", "GET", "PATCH", "DELETE"])
@reseller_required
def organizations(organization=None):
    if organization is not None and request.method == "GET":
        return _getOrgInfo(organization)
    if request.method in {"POST", "PATCH", "DELETE"}:
        return _modOrg(organization)
    return _getAllOrgs()
    pass

def _getOrgInfo(organization):
    organization = _retrieveOrg(organization)
    return jsonify(**organization.serialize())

def _modOrg(organization):
    if request.method == "POST":
        name = request.form["name"]
        try:
            newOrg = Organization.Create(name=name, reseller=request.reseller)
            pass
        except OrganizationExists:
            return jsonify(status="failed", reason="organization with name {0} already exists".format(name)), 409
        return jsonify(**newOrg.serialize()), 201
    if request.method == "PATCH":
        organization = _retrieveOrg(organization)
        orgName = request.form.get("name", organization.name)
        vendor = request.form.get("vendor", request.reseller.id)
        vendor = Reseller.query.filter(Reseller.id == vendor).first()
        if vendor is None:
            return jsonify(status="failed", reason="vendor not found"), 404
        organization.name = orgName
        organization.reseller = vendor
        organization.save()
        return jsonify(**organization.serialize())
    if request.method == "DELETE":
        organization = _retrieveOrg(organization)
        organization.delete()
        return jsonify(status="success", id=organization.id)
    pass

def _getAllOrgs():
    orgs = []
    for organization in request.reseller.organizations:
        orgs.append(organization.serialize())
        pass
    return Response(json.dumps(orgs), headers={"Content-Type": "application/json"})

def _retrieveOrg(orgID):
    organization = Organization.query.filter(Organization.id == orgID).first()
    if organization is None:
        abort(404)
    return organization

## TODO: move this
@shuttlOrgs.route('/getStaticContent/<file_id>', methods=['GET'])
@organization_required
def getFile(file_id):
    try:
        fileObj = FileObject.polyQuery().filter(FileObject.id==file_id).first().cast()
    except AttributeError:
        abort(404)
    return fileObj.buildResponse()

## This is an api endpoint for the organizations to modify the users
@csrf.exempt
@shuttlOrgs.route("/user", methods=["POST", "GET"])
@shuttlOrgs.route("/user/<userID>", methods=["POST", "GET", "PATCH", "DELETE"])
@organization_required
def users(userID=None):
    if userID is not None and request.method == "GET":
        return _getUserInfo(request.organization.id, userID)
    if request.method in {'POST', "PATCH", "DELETE"}:
        return _modUser(request.organization.id, userID)
        pass
    return _getAllUsers(request.organization.id)

def _getUserInfo(orgID, userID):
    user_obj = _retrieveUser(orgID, userID)
    return jsonify(**user_obj.serialize())


def _modUser(orgID, userID):
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        try:
            org = Organization.query.filter(Organization.id == orgID).first()
            newUsr = User.Create(organization=org, username=username, password=password, email=email)
            pass
        except UserDataTakenException:
            return jsonify(status="failed", reason="user with name {0} already exists".format(username)), 409
        return jsonify(**newUsr.serialize()), 201

    if request.method == "PATCH":
        user = _retrieveUser(orgID, userID)

        username = request.form.get("username", user.username)
        password = request.form.get("password", user.password)
        firstName = request.form.get("firstName", user.firstName)
        lastName = request.form.get("lastName", user.lastName)
        email = request.form.get("email", user.email)
        isActive = request.form.get("isActive", user.isActive)
        isAdmin = request.form.get("isAdmin", user.isAdmin)
        isFree = request.form.get("isFree", user.isFree)
        isContact = request.form.get("isContact", user.isContact)

        organization = request.form.get("organization", user.organization)
        organization = Organization.query.filter(Organization.id==organization).first()

        user.organization = organization
        user.username = username
        user.setPassword(password)
        user.firstName = firstName
        user.lastName = lastName
        user.email = email
        user.isActive = isActive
        user.isAdmin = isAdmin
        user.isFree = isFree
        user.isContact = isContact
        user.save()
        return jsonify(**user.serialize())
    if request.method == "DELETE":
        user = _retrieveUser(orgID, userID)
        user.delete()
        return jsonify(status="success", id=user.id)
    pass

def _retrieveUser(orgID, usrID):
    org = _retrieveOrg(orgID)
    user = User.query.filter(User.id==usrID).first()
    if user is None:
        abort(404)
    if org == user.organization:
        return user
    abort(404)
    pass

def _getAllUsers(orgID):
    org = _retrieveOrg(orgID)

    all_users = User.query.filter(User.organization==org).all()

    users_in_organization = []
    for user in all_users:
        if org == user.organization:
            users_in_organization.append(user.serialize())
            pass
        pass
    return Response(json.dumps(users_in_organization), headers={"Content-Type": "application/json"})
