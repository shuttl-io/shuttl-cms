from flask import render_template, request, jsonify, Response, abort
import json
from sqlalchemy.exc import IntegrityError

from shuttl import csrf
from shuttl.misc import shuttlOrgs
from shuttl.MiddleWare.OrganizationMiddleware import subdomain_login_required, organization_required
from shuttl.Models.Website import Website
from shuttl.Models.FileTree.TreeNodeObject import TreeNodeObject
from shuttl.Models.FileTree.FileObjects.FileObject import FileObject


@shuttlOrgs.route("/render/<website_id>/<page_id>/", methods=['GET'])
@shuttlOrgs.route("/render/<website_id>/", methods=['GET'])
@subdomain_login_required
def render(website_id, page_id=None):
    website = Website.query.filter(Website.id == website_id).first()
    if website is None or website.organization != request.organization:
        abort(404)
        pass
    if page_id is None:
        return render_template("website/dashboard.html", website=website, organization=request.organization)
    file = TreeNodeObject.polyQuery().filter(TreeNodeObject.id == page_id).first()
    if file is None:
        abort(404)
        pass
    if type(file) == FileObject:
        file = file.cast()
        pass
    if file.fileType == 'image':
        return file.buildResponse()
    content = file.buildContent(website=website, page=file, organization=request.organization)
    if file.fileType != "page":
        content = render_template("website/file_editor_renderer.html", website=website, content=content, file=file)
        pass
    return content


@shuttlOrgs.route("/show/<website_id>/<page_id>/", methods=['GET'])
@shuttlOrgs.route("/show/<website_id>/", methods=['GET'])
@subdomain_login_required
def showContent(website_id, page_id=None):
    website = Website.query.filter(Website.id == website_id).first()
    if website is None or website.organization != request.organization:
        abort(404)
        pass
    page = page_id
    directory = website.root
    try:
        page = TreeNodeObject.polyQuery().filter(TreeNodeObject.id == page).first()
        directory = page.parent
        pass
    except AttributeError:
        pass
    if directory is None:
        abort(404)
        pass
    return render_template("website/content.html",
        website=website,
        page=page,
        organization=request.organization,
        current_dir=directory.id,
        dropDownItems=request.organization.getDropDownItems(website)
    )


@csrf.exempt
@shuttlOrgs.route("/websites/", methods=["GET", "POST"])
@shuttlOrgs.route("/websites/<website_id>", methods=["GET", "PATCH", "DELETE"])
@organization_required
def websites(website_id=None):
    if request.method == "GET":
        if website_id is None:
            return _getAllWebsites()
        else:
            return _getWebsite(website_id)
    if request.method == "POST":
        return _createWebsite(request.form)
    if request.method == "PATCH":
        return _updateWebsite(website_id)
    if request.method == "DELETE":
        return _deleteWebsite(website_id)


def _createWebsite(form):
    name = form["name"]
    name = name.strip()
    if name == "":
        return jsonify(status="fail", reason="name is empty")
    try:
        website = Website.Create(organization=request.organization, name=name)
        return jsonify(**website.serialize()), 201
    except IntegrityError:
        return jsonify(status="failed", reason="websites with name {0} already exists".format(name)), 409
    pass


def _getAllWebsites():
    sites = list()
    for website in request.organization.websites:
        sites.append(website.serialize())
        pass
    return Response(json.dumps(sites), headers={"Content-Type": "application/json"})


def _getWebsite(website_id):
    website = Website.query.filter(Website.id == website_id).first()
    if website is None:
        return jsonify(status="fail", reason="website does not exist"), 404
    return jsonify(**website.serialize())


def _updateWebsite(website_id):
    website = Website.query.filter(Website.id == website_id).first()
    if website is None:
        return jsonify(status="fail", reason="website does not exist"), 404
    website.name = request.form.get("name", website.name)
    website.save()
    return jsonify(**website.serialize())


def _deleteWebsite(website_id):
    website = Website.query.filter(Website.id == website_id).first()
    if website is None:
        return jsonify(status="fail", reason="website does not exist"), 404
    website.delete()
    return jsonify(status="ok"), 200
