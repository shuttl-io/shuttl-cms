from flask import render_template, request, redirect, url_for, jsonify, Response
from flask.ext.login import login_user, logout_user, login_required, current_user
import json
import requests

from sqlalchemy.exc import IntegrityError

from shuttl import csrf, db, app
from shuttl.misc import shuttl, shuttlOrgs
from shuttl.Models.User import User, UserDataTakenException
from shuttl.Models.organization import Organization, OrganizationExists, OrganizationDoesNotExistException
from shuttl.Models.Website import Website
from shuttl.Models.FileTree.FileObjects import FileObject
from shuttl.MiddleWare.OrganizationMiddleware import organization_required, subdomain_login_required, reseller_required
from shuttl.Views import redirect_subdomain
from shuttl.Forms.OrganizationSignupForm import OrganizationSignupForm
from shuttl.Forms.LoginForm import LoginForm
from shuttl.Models.Validators.OrganizationValidator import OrganizationValidator

msg = {
    '-1': 'This username is already taken.',
    '-2': 'This email is taken'
}


@shuttlOrgs.route("/signup", methods=["POST", "GET"])
@organization_required
def signup():
    if current_user.is_authenticated and request.organization.containsUser(user=current_user):
        return redirect(url_for('shuttlOrgs.dashboard', organization=request.organization.sys_name))
    else:
        if request.organization.name != "demo" and not app.config["TESTING"]:
            return redirect(url_for('shuttlOrgs.dashboard', organization="demo"))
        form = OrganizationSignupForm()
        form.organization = request.organization
        err = request.args.get('error')
        if(err):
            print(type(err))
            return render_template('signup.html', form=form, error=msg.get(err, "There was an unknown error"))
        if form.validate_on_submit():
            try:
                user = form.save()
                return redirect(url_for('shuttlOrgs.confirm', organization=request.organization.sys_name, email=user.email))
            except UserDataTakenException as e:
                return redirect(url_for('shuttlOrgs.signup', organization=request.organization.sys_name, error=e.code))
        return render_template('signup.html', form=form)


@shuttlOrgs.route("/confirm/<email>")
@organization_required
def confirm(email):
    return render_template('checkEmail.html', email=email)


@shuttlOrgs.route("/validate/<string:token>", methods=["POST", "GET"])
@organization_required
def validate(token):
    if current_user.is_authenticated:
        return redirect(url_for('shuttlOrgs.dashboard', organization=request.organization.sys_name))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = form.loadUser(request.organization)
            if user is None:
                return redirect(url_for("shuttlOrgs.validate", token=token, organization=request.organization.sys_name, error=-1))
            OrganizationValidator.Validate(token=token, user=user)
            login_user(user, remember=True)
            return redirect(url_for("shuttlOrgs.dashboard", organization=request.organization.sys_name))
        return render_template("vendors/validate.html", organization=request.organization.sys_name, token=token, form=form)


@shuttlOrgs.route('/login', methods=['GET', 'POST'])
@organization_required
def login():
    if current_user.is_authenticated and (request.organization.containsUser(user=current_user)):
        return redirect(url_for('shuttlOrgs.dashboard', organization=request.organization.sys_name))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = form.loadUser(request.organization)
            if user is None:
                return render_template("login.html", form=form, error='Invalid email or password')
            login_user(user, remember=True)
            return redirect(url_for("shuttlOrgs.dashboard", organization=request.organization.sys_name))
        return render_template('login.html', form=form)


@shuttlOrgs.route('/logout')
@organization_required
def logout():
    logout_user()
    return redirect(url_for('shuttlOrgs.login', organization=request.organization.sys_name))


@shuttl.route('/create', methods=['GET', 'POST'])
def create():
    error = None
    if request.args.get('org') is not None:
        error = request.args.get('org')
    if request.method == 'POST':
        try:
            org = Organization.Create(request.form['organization'])
            User.Create(org, request.form['password'],
                        username=request.form['username'], email=request.form['email'])
            # return redirect_subdomain(url_for("shuttlOrgs.login"), request.url, org.name)
            return (url_for("shuttlOrgs.login", organization=org.name))
        except OrganizationExists:
            return redirect('/create?e=100&org=' + request.form['organization'])
        pass
    return render_template('create.html', error=error)


@shuttlOrgs.route('/github-login', methods=['GET', 'POST'])
@organization_required
def githubLogin():
    redirect_uri = url_for('shuttl.githubRedirect', organization=request.organization.sys_name)
    return redirect('https://github.com/login/oauth/authorize?client_id={}&redirect_uri={}&scope={}'
                .format(app.config["GITHUB_CLIENT_ID"], redirect_uri, 'user'))


@shuttl.route('/<organization>/github-redirect', methods=['GET', 'POST'])
def githubRedirect(organization):
    return redirect(url_for("shuttlOrgs.githubOrganizationRedirect", organization=organization, code=request.args.get('code')))


@shuttlOrgs.route('/github-redirect', methods=['GET', 'POST'])
@organization_required
def githubOrganizationRedirect():
    payload = {'client_id': app.config["GITHUB_CLIENT_ID"], 'client_secret': app.config["GITHUB_CLIENT_SECRET"], 'code': request.args.get('code')}
    headers = {"Accept": 'application/json'}
    response = requests.post('https://github.com/login/oauth/access_token', params=payload, headers=headers)
    access_token = json.loads(response.text)["access_token"]
    auth_header = {"Authorization": 'token {}'.format(access_token), "Accept": 'application/json'}
    ##grab the user's possible emails, filter out the verified and primary email AND the username
    user_response = requests.get('https://api.github.com/user', headers=auth_header)
    email_response = requests.get('https://api.github.com/user/emails', headers=auth_header)
    github_username = json.loads(user_response.text)['login']
    primary_email = None
    email_list = json.loads(email_response.text)
    for email in email_list:
        if email['verified'] is True and email['primary'] is True:
            primary_email = email['email']
            break
        pass
    else:
        primary_email = email_list[0]["email"]
        pass
    user = User.query.filter(User.email == primary_email).filter(User.organization_id == request.organization.id).first()
    if user is None:
        if request.organization.name != "demo":
            return redirect(url_for('shuttlOrgs.dashboard', organization="demo"))
        user = User.Create(organization=request.organization, username=username(github_username,
                request.organization), email=primary_email, isActive=True)
        user.sendHelloEmail()
    user.githubAccessToken = access_token
    user.save()
    login_user(user, remember=True)
    return redirect(url_for('shuttlOrgs.dashboard', organization=request.organization.sys_name))


@shuttlOrgs.route('/home', methods=['GET'])
@subdomain_login_required
def dashboard():
    return render_template('dashboard.html')

## helper function to recursively generate a username if already taken
## appends a number to the end of the original username
def username(github_username, organization, number=0):
    usr_name = "{0}{1}".format(github_username, number if number != 0 else "")
    user_exists = organization.containsUser(usr_name)
    if user_exists:
        return username(github_username, organization, number + 1)
    return usr_name
