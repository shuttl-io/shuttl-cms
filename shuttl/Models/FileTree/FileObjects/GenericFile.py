from .FileObject import FileObject
from flask import send_from_directory
from shuttl import db

class GenericFile(FileObject):

    ##Id of the css. Because of the way inheritance is set up in sqlalchemy, this is a foreignKey
    id = db.Column(db.Integer, db.ForeignKey('file_object.id'), primary_key=True)

    ## The Type of File
    _fileType = ""

    ## The Extension of the file
    fileExt = ""

    __mapper_args__ = {
        'polymorphic_identity': 'generic_file',
    }

    def _getUploadPath(self):
        return "generic/"

    def render(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.fileType,
            "sys_name": self.sys_name
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

    def headers(self):
        return {'Content-Type': 'text/plain'}

    def save(self):
        file_parts = self.name.rsplit('.', 1)
        if len(file_parts) > 1:
            self.fileExt = file_parts[-1]
        super(GenericFile, self).save()
