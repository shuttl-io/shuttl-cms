from jinja2 import Environment, FileSystemLoader
import os
from flask import Response

from .FileObject import FileObject
from shuttl import db

## A class that represents a template
class Template(FileObject):

    ##Id of the template. Because of the way inheritance is set up in sqlalchemy, this is a foriegnKey
    id = db.Column(db.Integer, db.ForeignKey('file_object.id'), primary_key=True)

    ##The fileType of the object
    _fileType = 'twig'

    ##The fileExt of the object
    fileExt = 'html'

    webpages = db.relationship('Webpage', back_populates='template')

    ## Tell the mapper that for fileType=template, cast into a template object
    __mapper_args__ = {
        'polymorphic_identity': 'template',
    }

    ## Gets the textual representation of the Object
    #
    # \return <Template: Object_name>"
    def __str__(self):
        return '<Template: {0}>'.format(self.name)

    ## Gets the headers of the file
    # \return the file headers
    def headers(self):
        return {'Content-Type': 'text/plain'}

    ## Builds the content of the file.
    # \param context the context of the request, used to build the Page
    # \return the built content
    def buildContent(self, context=None, render=False, **kwargs):
        if render:
            if context is None:
                context = dict()
                pass
            from shuttl.Templates.Tags import load_tags
            from shuttl.Templates.Loader import ShuttlLoader
            env = Environment(loader=ShuttlLoader(self.website))
            load_tags(env)
            env.prevRendered = set()
            context.update(**kwargs)
            temp = env.get_template(self.fullPath)
            return temp.render(**context)
        content = ""
        with self.file as fi:
            content = fi.read()
            pass
        return content

    ## Builds the response for sending the file
    # \return the built response
    def buildResponse(self):
        return Response(self.buildContent(), headers=self.headers())

    ## Get where the file belongs on the server
    # \return the place to save the file
    def _getUploadPath(self):
        return 'templates/'

    ## Dictionary representation of object
    # \return dictionary with template member variables
    def render(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.fileType,
            'sys_name': self.sys_name
        }

    def publish(self, publisher):
        publisher.publishFile(self)
        pass

    pass
