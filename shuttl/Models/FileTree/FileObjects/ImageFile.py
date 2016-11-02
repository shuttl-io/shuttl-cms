import mimetypes
from flask import send_from_directory
from .FileObject import FileObject
from shuttl import db


class ImageFile(FileObject):
    id = db.Column(db.Integer, db.ForeignKey('file_object.id'), primary_key=True)

    ## The Type of File
    _fileType = "image"

    ## The Extension of the file
    fileExt = ""

    __mapper_args__ = {
        'polymorphic_identity': 'image_file',
    }

    def _getUploadPath(self):
        return "images/"

    ## the underlying file of the object, Opens for reading
    # \returns the file to read
    @FileObject.file.getter
    def file(self):
        return open(self.filePath, "rb")

    ## Renders the page for the FileMap
    # \return a dictionary defining the object
    def render(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.fileType,
            "sys_name": self.sys_name,
            "image_type": self.fileExt
        }

    ## Builds the content of the file.
    # \param context the context of the request, used to build the Page
    # \return the built content
    def buildContent(self, context=None, **kwargs):
        return self.file.read()

    ## Builds the response for sending the file
    # \return the built response
    def buildResponse(self):
        filename = self.filePath.split('/')[-1]
        return send_from_directory(self.getUploadPath(), filename)

    # Gets the headers of the file
    # \return the file headers
    def headers(self):
        mime_type = mimetypes.guess_type(self.fullPath)[0]
        return {'Content-Type': mime_type}

    ## Overrides the save to allow for grabbing the extension from the file
    def save(self):
        file_parts = self.name.rsplit('.', 1)
        self.fileExt = file_parts[-1]
        super(ImageFile, self).save()

    def serialize(self, *args, **kwargs):
        fileDict = super(ImageFile, self).serialize(*args, **kwargs)
        fileDict.pop('content')
        return fileDict
