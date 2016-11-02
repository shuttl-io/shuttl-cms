import jinja2
import time
import os

from shuttl.Models.FileTree.TreeNodeObject import BrokenPathError
from shuttl.Models.FileTree.FileObjects.Template import Template

##Loads a Template based on the Shuttl Path. This path is not the Same path as
# the server path.
class ShuttlLoader(jinja2.BaseLoader):

    ## __init__ function
    # \param website the website that we should load all templates from
    def __init__(self, website):
        self.website = website
        pass

    ## Gets the file contents of the template and returns that to be parsed by
    # jinja
    #
    # \param environment the Jinja environment that everything is loaded from
    # \param templateName the path of the template to load. For example, Shuttl
    # may store the template in media/templates/<uuid>.twig but shuttl knows
    # this file as /templates/base.html. This gets /templates/base.html and
    # returns the contents of media/templates/<uuid>.twig
    #
    # \return the return value is based off of http://jinja.pocoo.org/docs/dev/api/#jinja2.BaseLoader.get_source
    def get_source(self, environment, templateName):
        try:
            template = Template.GetFileFromPath(templateName, self.website)
            pass
        except (FileNotFoundError, BrokenPathError):
            raise jinja2.TemplateNotFound(templateName)
        try:
            mtime = os.path.getmtime(template.filePath)
            pass
        except FileNotFoundError:
            mtime = time.gmtime(0)
            pass
        source = template.fileContents
        return source, templateName, mtime == os.path.getmtime(template.filePath)
