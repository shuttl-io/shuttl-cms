from shuttl import db
from shuttl.Models.FileTree.FileObjects.FileObject import FileObject
from shuttl.Models.FileTree.Directory import Directory
from shuttl.database import BaseModel


##Class for the Websites
class Website(BaseModel, db.Model):

    ## name of the Website
    name = db.Column(db.String, nullable=False)
    
    ## name of the Website without spaces
    sys_name = db.Column(db.String, nullable=False)
    ##The organization this belongs to.
    organization_id = db.Column(db.Integer, db.ForeignKey("organization.id"), nullable=False)

    ##The id of the root dir
    root_id = db.Column(db.Integer, db.ForeignKey('directory.id'), nullable=False)

    ##The actuall root dir
    root = db.relationship("Directory", foreign_keys=[root_id], uselist=False)

    ##The id of the root dir
    hidden_id = db.Column(db.Integer, db.ForeignKey('directory.id'))

    ##The actuall root dir
    hidden = db.relationship("Directory", foreign_keys=[hidden_id], uselist=False)

    ##The actuall root dir
    publishers = db.relationship("BasePublisher", back_populates='website')

    files = db.relationship('TreeNodeObject', back_populates='website')

    __mapper_args__ = {
        'polymorphic_identity': 'website',
    }

    ## Makes name and organization unique together
    __table_args__ = (
        db.UniqueConstraint('name', 'organization_id', name='_name_org_uc'),
    )

    ## Initialize the object.
    # \param organization the organization this website belongs to
    # \param name the name of the website
    def __init__(self, organization, name):
        self.organization = organization
        self.name = name
        self.sys_name = self.name.replace(" ", "_")
        self.root = Directory(name='root')
        pass

    ## Overwrite save to set sys_name
    def save(self):
        self.sys_name = self.name.replace(" ", "_")
        super(Website, self).save()
        pass

    @classmethod
    def Create(cls, *args, **kwargs):
        inst = cls(*args, **kwargs)
        delete_root = inst.root
        root = Directory.Create(name='root', website=inst)
        hidden = Directory.Create(name='_hidden', isHidden=True, website=inst)
        root.addChild(hidden)
        inst.root = root
        delete_root.delete()
        inst.root.website = inst
        hidden.isHidden = True
        hidden.save()
        inst.hidden_id = hidden.id
        inst.save()
        return inst

    ## returns the whole sitemap
    # \return the sitemap starting at root
    def render(self):
        return self.root.render()

    def publish(self, publishObj=None):
        publishObj = publishObj or self.root
        FileObject.Sync()
        for publisher in self.publishers:
            publisher.setUpConnection()
            publishObj.publish(publisher)
            publisher.destroyConnection()
            pass
        pass

    ## Gets the directory at the path
    # \param path the path to the directory
    # \return the directory the coresponds to path or none if the directory doesn't exist
    def getDirectoryFromPath(self, path):
        pathParts = path.split("/")
        directory = self.root
        for i in pathParts:
            if i == "":
                continue
            directory = Directory.query.filter(Directory.parent_id == directory.id, Directory.name == i).first()
            if directory is None:
                return None
            pass
        return directory
