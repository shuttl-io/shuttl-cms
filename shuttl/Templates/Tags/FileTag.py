import os

from .Base import BaseTagExtension
from flask import url_for
from shuttl.Models.FileTree.FileObjects.FileObject import FileObject
from shuttl.Models.FileTree.Webpage import Webpage
from shuttl.Models.FileTree.TreeNodeObject import TreeNodeObject
from shuttl.Models.FileTree.FileObjects.CssFile import CssFile

class InvalidStaticFileExtensionException(Exception): pass
## The class for static tags
class FileTagExtension(BaseTagExtension):

    ## What tags trigger this extension
    tags = {'file'}

    ## Creates a tag for the script or returns the actual file
    # \param context the context rendering the content
    # \param name the name of the block
    # \param default the default content
    # \return the rendered file or the tag
    def _action(self, context, file):
        fileObj = None
        if context['publishing']:
            publisher = context['publisher']
            return os.path.join(publisher.relativeUrl, file)
        website = context['website']
        try:
            fileObj = TreeNodeObject.GetFileFromPath(file, website)
            if type(fileObj) == Webpage:
                return url_for("shuttlOrgs.showContent", website_id=website.id, page_id=fileObj.id, organization=website.organization.sys_name)
            url = url_for("shuttlOrgs.getFile", file_id=fileObj.id, organization=website.organization.sys_name)
            pass
        except FileNotFoundError:
            return url_for("shuttlOrgs.getFile", file_id=-1, organization=website.organization.sys_name)
        return url
