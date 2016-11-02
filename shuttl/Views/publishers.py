from flask import render_template, request, jsonify, Response, abort
import json

from sqlalchemy.exc import IntegrityError
from shuttl import csrf
from shuttl.misc import shuttlOrgs
from shuttl.MiddleWare.OrganizationMiddleware import subdomain_login_required, organization_required
from shuttl.Models.Website import Website
from shuttl.Models.Publishers.Base import BasePublisher
from shuttl.Models.Queue import Queue
from shuttl.Models.FileTree.TreeNodeObject import TreeNodeObject
from shuttl.Models.FileTree.FileObjects.FileObject import FileObject

def _retrieveWebsite(website_id):
    return Website.query.filter(Website.id == website_id).first()

def _retrievePublisher(website_id, publisher_id):
    return BasePublisher.query.filter(BasePublisher.website_id==website_id).filter(BasePublisher.id==publisher_id).first()

def _retrieveFile(file_id):
    obj = TreeNodeObject.polyQuery().filter(TreeNodeObject.website_id==website_id, TreeNodeObject.id==file_id).first()
    if obj is None:
        raise FileNotFoundError

# @csrf.exempt
# @shuttlOrgs.route("/websites/<website_id>/publishers/", methods=["GET", "POST"])
# @shuttlOrgs.route("/websites/<website_id>/publishers/<publisher_id>", methods=["GET", "PATCH", "DELETE"])
# @organization_required
# def publishers(website_id, publisher_id=None):
#     if request.method == "GET":
#         if publisher_id is None:
#             return _getAllWebsites()
#         else:
#             return _getWebsite(publisher_id)
#     if request.method == "POST":
#         return _createPublisher()
#     if request.method == "PATCH":
#         return _editPublisher(publisher_id)
#     if request.method == "DELETE":
#         return _deletePublisher(publisher_id)

@csrf.exempt
@shuttlOrgs.route("/websites/<website_id>/publish", methods=["POST"])
@shuttlOrgs.route("/websites/<website_id>/files/<file_id>/publish", methods=["POST"])
@organization_required
def publish(website_id, file_id=None):
    try:
        obj = {"website": _retrieveWebsite(website_id)} if file_id is None else {"fileObject": _retrieveFile(file_id)}
        pass
    except FileNotFoundError:
        return jsonify(status='failed', reason='The object is not found'), 404
    entry = Queue.Push(**obj)
    return jsonify(status='ok', entry_id='publish_task_{0}'.format(entry.id)), 201
