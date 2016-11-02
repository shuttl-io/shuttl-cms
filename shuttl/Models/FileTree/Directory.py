from shuttl import db
from .TreeNodeObject import TreeNodeObject

## A class That represents a directory
class Directory(TreeNodeObject):

    ##Id of the directory. Because of the way inheritance is set up in sqlalchemy, this is a foriegnKey
    id = db.Column(db.Integer, db.ForeignKey('tree_node_object.id'), primary_key=True)

    ## A dir object can have children
    canHaveChildren = True

    ##The fileType of the object
    fileType = "dir"

  ## Tell the mapper that for fileType=directory, cast into a directory object
    __mapper_args__ = {
        'polymorphic_identity': 'directory',
    }

    ## Adds a child directory. basically it just calls the Directory.Create method (Inherited from BaseModel)
    # followed by the Directory.addChild (inherited from FileTreeObject)
    #
    # \param name the name of the directory to call
    # \return the created dir
    #
    # \sa shuttl.database.BaseModel
    # \sa shuttl.Models.FileTreeObject
    def addChildDir(self, name, website):
        dir = Directory.Create(name=name, website=website)
        self.addChild(dir)
        return dir

    @property
    def __json__(self):
        res = super(Directory, self).__json__
        res.add("children")
        return res

    ## Gets the Textual representation of the Object
    #
    # \return <Directory: Object_name>"
    def __str__(self):
        return "<Directory: {0}>".format(self.name)

    ## Renders the file directory structure starting at this object (AKA this Node). Calls render recursively to build
    # a dictionary that represents the entire tree rooted at this Node
    #
    # \return a dictionary laid out like this:
    #   id: the id of the object
    #   name: the Name of the object
    #   fileType the Type of the object
    #   sys_name: the sys_name of the object
    #   children: the children render results
    def render(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.fileType,
            "sys_name": self.sys_name,
            "children": [i.render() for i in self.children]
        }

    def publish(self, publisher):
        publisher.publishDirectory(self)
        for child in self.children:
            child.publish(publisher)
            pass
        pass

    pass