from flask import request, jsonify, Response, render_template
from werkzeug.datastructures import FileStorage
from sqlalchemy.exc import IntegrityError
from tempfile import NamedTemporaryFile
import os
import json

from shuttl import csrf
from shuttl.misc import shuttlOrgs
from shuttl.MiddleWare.OrganizationMiddleware import organization_required
from shuttl.Models.FileTree.FileObjects.FileObject import FileObject
from shuttl.Models.FileTree.FileObjects.Template import Template
from shuttl.Models.FileTree.FileObjects.GenericFile import GenericFile
from shuttl.Models.Website import Website
from shuttl.Models.FileTree.Directory import Directory
from shuttl.Models.FileTree.Webpage import Webpage
from shuttl.Models.ContentBlocks.GlobalBlock import GlobalBlock
from shuttl.Models.FileTree.TreeNodeObject import TreeNodeObject
from shuttl.Models.ContentBlocks.MultipleBlock import MultipleBlock

@csrf.exempt
@shuttlOrgs.route('/website/<website_id>/files/', methods=['GET'])
@shuttlOrgs.route('/website/<website_id>/files/<file_type>/', methods=['GET', 'POST'])
@shuttlOrgs.route('/website/<website_id>/files/<file_type>/<file_id>/', methods=['GET', 'PATCH', 'DELETE'])
@organization_required
def files(website_id=None, file_type=None, file_id=None):
    file_dictionary = {n._fileType: n for n in FileObject.__subclasses__()}
    file_dictionary.update({Webpage.fileType: Webpage, Directory.fileType: Directory})
    if request.method == 'GET':
        if file_type is None and file_id is None:
            return _getAllFiles(website_id)
        elif file_id is None:
            return _getFilesByType(website_id, file_type, file_dictionary)
        else:
            return _getFile(website_id, file_type, file_id, file_dictionary)
    if request.method == 'POST':
        return _createFile(website_id, file_type, request, file_dictionary)
    if request.method == 'PATCH':
        return _updateFile(website_id, file_type, file_id, request.form, file_dictionary)
    if request.method == 'DELETE':
        return _deleteFile(website_id, file_type, file_id, file_dictionary)


def _createFile(website_id, file_type, request, file_dictionary):
    try:
        if file_type == "html":
            file_type = "twig"
            pass
        if file_type in ('jpg', 'png', 'jpeg'):
            file_type = 'image'
        klass = file_dictionary.get(file_type, GenericFile)
    except KeyError:
        print(file_dictionary.keys())
        return jsonify(status='failed', reason='invalid class type {0}'.format(file_type)), 404
    form = request.form
    files = request.files
    name = form['name']
    parent_id = form['parent_id']
    website = Website.query.filter(Website.id == website_id).first()
    dir = Directory.query.filter(Directory.id == parent_id).first()
    if 'file_contents' in form:
        content = form['file_contents']
        fi = NamedTemporaryFile(delete=False, suffix='.{0}'.format(file_type))
        fi.write(str.encode(content))
        fi.close()
        with open(fi.name, 'rb') as fp:
            file = FileStorage(fp)
            try:
                newfile = klass.Create(parent=dir, file=file, name=name, website=website)
            except IntegrityError:
                return jsonify(status='failed', reason='file named {0}.{1} already exists'.format(name, file_type)), 409
        os.unlink(fi.name)
    elif 'file' in files:
        try:
            newfile = klass.Create(parent=dir, file=files['file'], name=name, website=website)
        except IntegrityError:
            return jsonify(status='failed', reason='file named {0} already exists'.format(name)), 409
    elif file_type == "dir":
        newfile = klass.Create(parent=dir, name=name, website=website)
        pass
    elif file_type == "page":
        template = Template.query.filter(Template.id == form["template_id"]).first()
        newfile = klass.Create(parent=dir, name=name, website=website, template=template)
    else:
        return jsonify(status='failed', reason='No files contents or file specified'.format(file_type)), 404
    return jsonify(**newfile.serialize()), 201


def _getAllFiles(website_id):
    fileObjQueryList = TreeNodeObject.polyQuery().filter(TreeNodeObject.website_id==website_id).filter(TreeNodeObject.isHidden==False)
    fileObjList = [file.serialize() for file in fileObjQueryList]
    return Response(json.dumps(fileObjList), headers={'Content-Type': 'application/json'}), 200


def _getFilesByType(website_id, file_type, file_dictionary):
    try:
        klass = file_dictionary.get(file_type, GenericFile)
    except KeyError:
        return jsonify(status='failed', reason='invalid class type {0}'.format(file_type)), 409
    fileObjQueryList = klass.polyQuery().filter(klass.website_id==website_id).filter(klass.isHidden==False)
    fileObjList = [file.serialize() for file in fileObjQueryList]
    return Response(json.dumps(fileObjList), headers={'Content-Type': 'application/json'}), 200


def _getFile(website_id, file_type, file_id, file_dictionary):
    try:
        klass = file_dictionary.get(file_type, GenericFile)
    except KeyError:
        return jsonify(status='failed', reason='invalid class type {0}'.format(file_type)), 409
    try:
        fileObj = klass.polyQuery().filter(klass.website_id==website_id, klass.id==file_id).filter(TreeNodeObject.isHidden==False).first()
    except AttributeError:
        return jsonify(status='failed', reason='no files'), 409
    if fileObj is None:
        return jsonify(status='failed', reason='no {0} file with id {1}'.format(file_type, file_id)), 404
    return jsonify(**fileObj.serialize()), 201


def _updateFile(website_id, file_type, file_id, form, file_dictionary):
    content, name = None, None
    contentForm = dict()
    if request.data != b'':
        contentForm = json.loads(request.data.decode())
        pass
    if 'file_contents' in form:
        content = form['file_contents']
        pass
    elif "file_contents" in contentForm:
        content = contentForm.get("file_contents")
    if 'name' in form:
        name = form['name']
    try:
        klass = file_dictionary.get(file_type, GenericFile)
    except KeyError:
        return jsonify(status='failed', reason='invalid class type {0}'.format(file_type)), 404
    fileObj = klass.polyQuery().filter(klass.website_id==website_id, klass.id==file_id).first()
    if fileObj is None:
        return jsonify(status='failed', reason='no {0} file with id {1}'.format(file_type, file_id)), 404
    if name is not None:
        fileObj.name = name
        pass
    if content is not None:
        if type(content) == dict:
            fileObj.updateContent(content["local"])
            for key, value in content.get("global", dict()).items():
                block = GlobalBlock.query.get(key)
                block.updateContent(value)
                pass
            pass
        else:
            fileObj.updateContent(content)
            pass
    try:
        fileObj.save()
        pass
    except IntegrityError:
        return jsonify(status='failed', reason='file with name {0} already exists'.format(file_type)), 409
    return jsonify(status='success', reason='{0} was modified'.format(fileObj.name))


def _deleteFile(website_id, file_type, file_id, file_dictionary):
    file_dictionary = {n._fileType: n for n in FileObject.__subclasses__()}
    file_dictionary.update({Webpage.fileType: Webpage, Directory.fileType: Directory})
    try:
        klass = file_dictionary.get(file_type, GenericFile)
    except KeyError:
        return jsonify(status='failed', reason='invalid class type'.format(file_type)), 409
    fileObj = klass.query.filter(klass.website_id==website_id, klass.id==file_id).first()
    if fileObj is None:
        return jsonify(status='failed', reason='file does not exist'), 404
    if fileObj.fileType == 'dir':
        fileObj.setForDeletion = True
        return jsonify(status='success', reason='{0} was deleted'.format(fileObj.name))
    fileObj.delete()
    return jsonify(status='success', reason='{0} was deleted'.format(fileObj.name))

def _retrieveWebsite(website_id, throw=True, returnVal=None):
    website = Website.query.filter(Website.id == website_id).first()
    if website is None:
        if throw:
            if returnVal is None:
                abort(404)
                return
            pass
        return returnVal
    return website

@csrf.exempt
@shuttlOrgs.route('/<website_id>/createFile/', methods=['GET'])
@shuttlOrgs.route('/<website_id>/createFile/<directory_id>', methods=['GET'])
@organization_required
def createFile(website_id, directory_id=None):
    website = _retrieveWebsite(website_id)
    directory = Directory.query.filter(Directory.id ==directory_id).first()
    if directory is None:
        directory = website.root
        pass
    return render_template("website/createFile.html", website=website, current_dir=directory.id, dropDownItems = request.organization.getDropDownItems(website))

@csrf.exempt
@shuttlOrgs.route('/website/<website_id>/page/<page_id>/multiBlocks/<name>', methods=['POST'])
@shuttlOrgs.route('/website/<website_id>/page/<page_id>/multiBlocks/<name>/<index>', methods=['POST', "DELETE"])
@organization_required
def multiblock(website_id, page_id, name, index=-1):
    index = int(index)
    website = _retrieveWebsite(website_id)
    page = Webpage.query.filter(Webpage.id == page_id).first()
    if page is None:
        abort(404)
        pass
    block = MultipleBlock.query.filter(MultipleBlock.webpage == page, MultipleBlock.name == name).first()
    action = block.append if request.method == "POST" else block.remove
    action(index)
    context = dict(
        website=website,
        page=page,
        organization=request.organization,
        current_dir = page.parent.id
    )
    return block.renderContent(context)