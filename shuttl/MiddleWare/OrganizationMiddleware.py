from flask import abort, request, redirect, url_for
from flask.ext.login import current_user, login_required, AnonymousUserMixin
from functools import wraps

from shuttl.Models.organization import Organization, OrganizationDoesNotExistException
from shuttl.Views import redirect_subdomain
from shuttl.Models.Reseller import Reseller, ResellerDoesNotExist

def reseller_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        hostname = request.headers.get("host")

        try:
            request.reseller = Reseller.GetNameFromHost(hostname)
            pass
        except ResellerDoesNotExist:
            pass
        return func(*args, **kwargs)
    return wrapper

def reseller_login(func):
    @reseller_required
    @login_required
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user not in request.reseller.admins:
            return url_for("shuttl.login")
        return func(*args, **kwargs)
    return wrapper

def organization_required(func):
    @wraps(func)
    def wrapper(organization, *args, **kwargs):
        try:
            reseller = Reseller.query.filter(Reseller.name == "shuttl").first()
            request.organization = Organization.Get(name= organization.replace("_", " "), vendor = reseller)
            pass
        except OrganizationDoesNotExistException:
            abort(404)
        return func(*args, **kwargs)
    return wrapper

def subdomain_login_required(func):
    @organization_required
    @login_required
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_in_organization = request.organization.containsUser(user=current_user)
        # organization = (user_in_organization is None or type(current_user) == AnonymousUserMixin)
        # vendor = (current_user.reseller is None or current_user.reseller != request.organization.reseller)
        # if organization and vendor:
        if not current_user.is_authenticated and user_in_organization is None: 
            return redirect(url_for("shuttlOrgs.login", organization=request.organization.sys_name))
        return func(*args, **kwargs)
    return wrapper
