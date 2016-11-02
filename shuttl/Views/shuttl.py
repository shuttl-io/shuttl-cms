from flask import render_template, redirect, url_for, request
from flask.ext.login import current_user, AnonymousUserMixin

from shuttl import app
from shuttl.misc import shuttl, shuttlOrgs
from shuttl.MiddleWare.OrganizationMiddleware import subdomain_login_required, organization_required


@shuttl.route('/')
def index():
    return render_template('index.html')

@shuttlOrgs.route('/')
@organization_required
def index():
    if current_user.is_authenticated:
        return redirect(url_for("shuttlOrgs.dashboard", organization=request.organization.sys_name))
    return redirect(url_for("shuttlOrgs.login", organization=request.organization.sys_name))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
