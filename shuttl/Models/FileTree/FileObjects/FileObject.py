import logging

from shuttl import db, app
from shuttl.Storage import Storage
from shuttl.Models.FileTree.TreeNodeObject import TreeNodeObject
from shuttl.Models.FileTree.Directory import Directory
from werkzeug import secure_filename
import uuid
from flask import abort
import os

## Base class for all objects that require a file (HTML, CSS, JS, Sass, ETC. . .)
class FileObject(TreeNodeObject):

    ##Id of the directory. Because of the way inheritance is set up in sqlalchemy, this is a foriegnKey
    id = db.Column(db.Integer, db.ForeignKey('tree_node_object.id'), primary_key=True)

    _fileType = "file"

    fileType = db.Column(db.String)

    ## the location of the file
    filePath = db.Column(db.String, nullable=False)

    ## Tell the mapper that for type=FileObject, cast into a FileObject object
    __mapper_args__ = {
        'polymorphic_identity': 'file_object',
    }

    ## the underlying file of the object, Opens for reading
    # \returns the file to read
    @property
    def file(self):
        if not os.path.isfile(self.filePath):
            Storage.Download(self)
            pass
        os.utime(self.filePath, None)
        return open(self.filePath, "r")

    @property
    def fileContents(self):
        content = None
        with self.file as fi:
            content = fi.read()
            pass
        return content

    @classmethod 
    def Sync(cls):
        for i in cls.query.all():
            Storage.Download(i)
            pass
        pass
        
    ## Sets the file
    # \param file, the new file
    @file.setter
    def file(self, file):
        filename = secure_filename(file.filename)
        _, extension = filename.rsplit(".", 1)
        filename = "{0}.{1}".format(uuid.uuid4(), extension)
        uploadTo = os.path.join(self.getUploadPath(), filename)
        file.save(uploadTo)
        self.filePath = uploadTo
        Storage.Upload(self)
        pass

    ## saves the content to the file
    # \param content the content to save
    def updateContent(self, content):
        self.writeToFile(content)
        pass

    ## Writes content to the file
    # \param content the content to go to the file
    def writeToFile(self, content):
        with open(self.filePath, "w+") as fi:
            os.utime(self.filePath, None)
            fi.write(content)
            pass
        Storage.Upload(self)
        pass 

    ## Gets the relative path where the file belongs, should be overloaded for each class
    # \return the place to save the file
    def _getUploadPath(self):
        return ""

    ## Gets the full path were the file belongs
    # \return the place to save the file
    def getUploadPath(self):
        parts = [app.config["UPLOAD_DIR"]]
        uploadPart = self._getUploadPath()
        if uploadPart != "":
            parts.append(uploadPart)
            pass
        return os.path.join(*parts)

    ## Gets the dir names of the path
    # \return a list of names all coresponding to a path list
    def _getPathParts(self):
        path = []
        dir = self.parent
        while dir is not None and dir.name != "root":
            path.append(dir.sys_name)
            dir = dir.parent
            pass
        return path[::-1]


    @property
    def __json__(self):
        res = super(FileObject, self).__json__
        res.add("fileType")

        return res

    ## the full path of the file object with the name (ie: /dir1/dir2/dir3/file.html)
    # \return the full path of the file object
    @property
    def fullPath(self):
        path = self._getPathParts()
        path.append(self.sys_name)
        return "/" + os.path.join(*path)

    ## Renders the page for the FileMap
    # \return a dictionary defining the object
    def render(self):
        raise NotImplementedError

    ## Get the path to the file, Doesn't include file name
    # \return the path to the file
    def resolvePath(self):
        path = self._getPathParts()
        return "/" + os.path.join(*path)

    ## Builds the content of the file.
    # \param context the context of the request, used to build the Page
    # \return the built content
    def buildContent(self, context, **kwargs):
        raise NotImplementedError

    ## Builds the response for sending the file
    # \return the built response
    def buildResponse(self):
        raise NotImplementedError

    ## Gets the headers of the file
    # \return the file headers
    def headers(self):
        raise NotImplementedError

    ## Gets the file or throws a 404 error.
    # \param *args could be anything
    # \return the file you're looking for
    # \raise 404 if the object is not found
    @classmethod
    def getItemOr404(cls, *args):
        itm = cls.polyQuery().filter(*args)
        if itm is None:
            abort(404)
            pass
        return itm

    @classmethod
    def Create(cls, parent, file, *args, **kwargs):
        kwargs["file"] = file
        kwargs["parent"] = parent
        inst = super(FileObject, cls).Create(*args, **kwargs)
        parent.children.append(inst)
        return inst

    ## Deletes the fileobject and removes the file if removeFile is True
    # \param removeFile, if true delete will delete the file as well.
    def delete(self, removeFile=False):
        if removeFile:
            os.remove(self.filePath)
            Storage.Delete(self)
            pass
        super(FileObject, self).delete()

    def save(self):
        self.fileType = self._fileType
        super(FileObject, self).save()
        pass

    @classmethod
    def LoadMapper(cls):
        FileObject.fileTypeMap = dict()
        for klass in FileObject.__subclasses__():
            FileObject.fileTypeMap[klass._fileType] = klass
            pass

    def publish(self, publisher):
        publisher.publishFile(self)
        pass
    pass

    def cast(self):
        return FileObject.fileTypeMap[self.fileType].query.get(self.id)

    def serialize(self, *args, **kwargs):
        fileDict = super(FileObject, self).serialize(*args, **kwargs)
        try:
            content = self.buildContent(dict())
        except NotImplementedError:
            content = None
            pass
        except FileNotFoundError:
            msg = """File Connection has been lost. Here are the details:
    File ID: {id}
    File Path: {path}
    File Name: {name}
    File Type: {type}
            """
            logging.error(msg.format(id=self.id, path=self.fullPath, name=self.name, type=self._fileType))
            content = "Error: File contents Lost"
            pass
        fileDict["content"] = content
        return fileDict


## A class to test FileObject
class FileObjectMock(FileObject):
    id = db.Column(db.Integer, db.ForeignKey('file_object.id'), primary_key=True)

    _fileType = "file_mock"

    fileType = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': 'fileobjectmock',
    }

    ## Get where the file belongs, should be overloaded for each object
    # \return the place to save the file
    # \raises NotImplementedError Because this function is meant to be implemented into the base class
    def _getUploadPath(self):
        return ""

    def render(self):
        return {"This": "rendered"}
