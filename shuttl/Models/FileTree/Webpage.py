import os
from bs4 import BeautifulSoup
from flask import url_for

from shuttl import db
from shuttl.Models.FileTree.TreeNodeObject import TreeNodeObject
from shuttl.Models.ContentBlocks.ContentBase import ContentBase
from shuttl.misc import ContentAttr


class Webpage(TreeNodeObject):

    ## id of the template. Because of the way inheritance is set up in sqlalchemy, this is a foriegnKey
    id = db.Column(db.Integer, db.ForeignKey('tree_node_object.id'), primary_key=True)

    ## file type
    fileType = 'page'

    # file extension
    fileExt = 'html'

    ## id of the template
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))

    ## template associated with the page
    template = db.relationship("Template", foreign_keys=[template_id], back_populates='webpages')

    ##The content blocks associated with this page
    contentBlocks = db.relationship("ContentBase", back_populates='webpage', cascade="all,delete")

    __mapper_args__ = {
        'polymorphic_identity': 'webpage',
    }

    ## Gets the textual representation of the Object
    #
    # \return <Directory: Object_name>"
    def __str__(self):
        return "<Webpage: {0}>".format(self.name)

    ## Builds the content/html of the page with the template associated with the page
    # \param publisher (optional), the publisher of the page
    # \return html from template and page content
    def buildContent(self, publisher=None, **kwargs):
        publishing =  publisher is not None
        context = {'page': self, "publishing": publishing, "publisher": publisher, "website": self.website}
        context.update(kwargs)
        data = self.template.buildContent(context, render=True)
        self._generalRendering(data)

        # If this is not being published, we need to add our internal JavaScript.
        if not publishing:
            data = self._internalRender(data)
            pass
        return data

    def _generalRendering(self, data):
        pass

    def _internalRender(self, data):
        #appends a script tag to the element
        import re as regex
        def addScriptTag(doc, src, element):
            script_tag = data_soup.new_tag("script", src=src, type="application/javascript")
            element.append(script_tag)
            pass
        data_soup = BeautifulSoup(data, "html.parser")
        pattern_a_tag = regex.compile(r'http[s]?:\/\/')
        for link in data_soup.find_all('a'):
            if pattern_a_tag.match(link['href']) is not None:
                link['target'] = '_blank'
            else:
                link['target'] = '_parent'
        head = data_soup.head
        body = data_soup.body
        if body is not None:
            addScriptTag(data_soup, "https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js", body)
            addScriptTag(data_soup, "//cdn.tinymce.com/4/tinymce.min.js", body)
            addScriptTag(data_soup, url_for('static', filename='js/internalMain.js'), body)
            addScriptTag(
                data_soup,
                url_for('static', filename='node_modules/tether-shepherd/dist/js/tether.js'),
                body
            )
            addScriptTag(
                data_soup,
                url_for('static', filename='node_modules/tether-shepherd/dist/js/shepherd.min.js'),
                body
            )
            pass
        if head is not None:
            css = data_soup.new_tag(
                "link",
                rel="stylesheet",
                type="text/css",
                href=url_for('static', filename='node_modules/tether-shepherd/dist/css/shepherd-theme-arrows.css')
            )
            head.append(css)
            css = data_soup.new_tag(
                "link",
                rel="stylesheet",
                type="text/css",
                href=url_for('static', filename='node_modules/tether-shepherd/dist/css/shepherd-theme-default.css')
            )
            head.append(css)
            pass
        return str(data_soup)

    # ## Not implemented yet, but will take in the context from a content block and save it
    # def saveChange(self, context):
    #     raise NotImplementedError

    ## saves the content to the file
    # \param content the content to save
    def updateContent(self, content):
        for blockName, blockValue in content.items():
            self[blockName] = blockValue
            pass
        pass


    ## Gets the headers of the file
    # \return the file headers
    def headers(self):
        return {'Content-Type': 'text/html'}

    ## Dictionary representation of object
    # \return dictionary with webpage member variables
    def render(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.fileType,
            'sys_name': self.sys_name
        }

    def __getitem__(self, item):
        from shuttl.Models.ContentBlocks.ContentBase import ContentBase
        content = ContentBase.GetOrCreate(webpage=self, name=item)
        if type(content) == ContentBase:
            raise IndexError("{0} item doesn't exist".format(item))
        return ContentBase.GetOrCreate(webpage=self, name=item)

    def __setitem__(self, key, value):
        content = ContentBase.GetOrCreate(webpage=self, name=key)
        content.setContent(value)
        pass

    def publish(self, publisher):
        publisher.publishFile(self)
        pass

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

    ## the full path of the file object with the name (ie: /dir1/dir2/dir3/file.html)
    # \return the full path of the file object
    @property
    def fullPath(self):
        path = self._getPathParts()
        path.append("{0}.{1}".format(self.sys_name, self.fileExt))
        return "/" + os.path.join(*path)

    ## Get the path to the file, Doesn't include file name
    # \return the path to the file
    def resolvePath(self):
        path = self._getPathParts()
        return "/" + os.path.join(*path)

    ## Gets the content
    # \return the content of the webpage
    @property
    def content(self):
        content = dict()
        for i in self.contentBlocks:
            content[i.name] = i.content
            pass
        return content
