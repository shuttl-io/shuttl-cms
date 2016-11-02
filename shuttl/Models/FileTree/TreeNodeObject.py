from flask import url_for
import os
from sqlalchemy.exc import IntegrityError

from shuttl import db
from shuttl.database import BaseModel
from shuttl.misc import AttrClass

class BrokenPathError(Exception): pass

class WebsiteNotSetException(Exception): pass

## An Abstract Base Class to represent objects in a directory structure
class TreeNodeObject(db.Model, BaseModel):
    ## Id of the file object
    id = db.Column(db.Integer, primary_key=True)

    ## the id of the parent object
    parent_id = db.Column(db.Integer, db.ForeignKey('tree_node_object.id'))

    ## Marks weather or not the asset is publishable.
    isPublishable = db.Column(db.Boolean, default=True)

    website_id = db.Column(db.Integer, db.ForeignKey('website.id', use_alter=True))

    website = db.relationship("Website", foreign_keys=[website_id], back_populates='files', post_update=True, uselist=False)

    shouldHaveWebsite = db.Column(db.Boolean, default=True)

    isHidden = db.Column(db.Boolean, default=False)

    ## The children of this class
    _children = db.relationship("TreeNodeObject",
                backref=db.backref('parent', remote_side=[id])
            )

    ## The Type of the object. Should be overridden in Derived classes.
    fileType = ""

    ## The file Extension for this file. Should be overridden in Derived classes.
    fileExt = ""

    ## name of the object
    name = db.Column(db.String)

    ## Type of the inherited class, this is used for polymorphic behavior
    type = db.Column(db.String(50))

    ## A flag indicating if the class can have children, this is true only on Directories
    canHaveChildren = False

    ## The arguments for the polymorphic behavior. SQLAlchemy link: http://docs.sqlalchemy.org/en/latest/orm/inheritance.html
    __mapper_args__ = {
        'polymorphic_identity':'tree_node_object',
        'polymorphic_on':type
    }

    ## Make name and parent_id unique together
    __table_args__ = (
        db.UniqueConstraint('name', 'parent_id', name='_name_parent_uc'),
        db.UniqueConstraint('id', 'parent_id', name='_id_parent_uc'),
    )

    context = dict()

    def setContext(self, context):
        self.context = context
        pass

    @property
    def path(self):
        pub = self.context.get("publishing", False)
        if not pub:
            path = url_for("shuttlOrgs.showContent", 
                website_id=self.website.id, 
                page_id=self.id, 
                organization=self.website.organization.sys_name
            )
            pass
        else: 
            path = os.path.join(self.context["publisher"].relativeUrl, self.fullPath)
            pass
        return path
    

    ## the full path of the file object with the name (ie: /dir1/dir2/dir3/file.html)
    # \return the full path of the file object
    @property
    def fullPath(self):
        path = self._getPathParts()
        if self.name == "root":
            return "/"
        path.append(self.sys_name)
        return "/" + os.path.join(*path)

    ## Gets the dir names of the path
    # \return a list of names all coresponding to a path list
    def _getPathParts(self):
        path = []
        dir = self.parent
        while dir is not None:
            if dir.name.lower() != "root":
                path.append(dir.sys_name)
                pass
            dir = dir.parent
            pass
        return path[::-1]

    @property
    def __json__(self):
        res = super(TreeNodeObject, self).__json__
        res.add("name")
        res.add("fullPath")
        res.discard("website")
        res.add("fileType")
        res.discard("_children")
        return res

    ##Adds a child to this FileTreeObject
    # \param obj the object to add a child
    # \raise Attribute Error if the Class can't have children
    def addChild(self, obj):
        if not self.canHaveChildren:
            raise AttributeError("'{0}' object has no attribute 'addChild'".format(self.__class__.__name__))
        if self.query.filter(TreeNodeObject.id == obj.id).filter(obj.parent_id == self.id).first():
            raise IntegrityError(statement="object already exsits", params=[obj.id, self.parent_id], orig="Here")
        obj.isHidden = self.isHidden
        obj.save()
        self._children.append(obj)
        self.save()
        pass

    ## Gets the object given a path (ie: /dir1/dir2/dir3/file.html)
    # \param path the path of the file
    # \param website The website the file should belong to
    @classmethod
    def GetFileFromPath(cls, path, website):
        from shuttl.Models.FileTree.Directory import Directory
        path_parts = path.split("/")
        dir = website.root
        for i in path_parts:
            if i == "" or i == path_parts[-1]:
                continue
            dir = Directory.query.filter(Directory.parent_id == dir.id, Directory.name == i).first()
            if dir is None:
                raise BrokenPathError(path)
            pass
        file = cls.polyQuery().filter(cls.parent_id == dir.id).filter(cls.name == path_parts[-1]).first()
        if file is None:
            raise FileNotFoundError(path)
        return file

    ## Gets all children associated with this class
    # \raise Attribute Error if the Class can't have children
    @property
    def children(self):
        if not self.canHaveChildren:
            raise AttributeError("'{0}' object has no attribute 'children'".format(self.__class__.__name__))
        return self._children

    ## Make a polymorphic Query, this will automatically cast objects to their inherited classes
    # \param cls_or_all defualts to ("*") this is the classes that we should cast to
    @classmethod
    def polyQuery(cls, cls_or_all=("*")):
        return cls.query.with_polymorphic(*cls_or_all)

    ## The sys_name of the file, just the name with the space replaced with underscores
    # \return the name with underscores
    @property
    def sys_name(self):
        return self.name.replace(" ", "_")

    ## render the object this is for making a visual representation of the class
    # \raise NotImplementedError
    # \note this should be implemented in derived classes
    def render(self):
        raise NotImplementedError

    def publish(self):
        raise NotImplementedError


    ## casts the object if needed
    # \return the object
    def cast(self):
        from .FileObjects.FileObject import FileObject
        if self.type is None:
            obj = FileObject.query.filter(FileObject.id == self.id).first()
            return obj
        return self
    pass


    def save(self):
        if self.website is not None or self.id is None or not self.shouldHaveWebsite:
            if self.parent and not self.isHidden:
                self.isHidden = self.parent.isHidden
                pass
            try:
                db.session.add(self)
                db.session.commit()
                pass
            except:
                db.session.rollback()
                raise
        else:
            raise WebsiteNotSetException
        pass

class TreeNodeMock(TreeNodeObject):
    id = db.Column(db.Integer, db.ForeignKey('tree_node_object.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'tree_mock',
    }
    pass
