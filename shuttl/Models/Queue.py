import datetime

from shuttl import db
from shuttl.database import BaseModel
from shuttl.Models.FileTree.TreeNodeObject import TreeNodeObject
from shuttl.Models.Website import Website

class InvalidEntryException(Exception): pass
class QueueIsEmptyException(Exception): pass

## Implements a Queue for the Publishing Queue
class Queue(BaseModel, db.Model):

    ##The file object to publish
    fileObject_id = db.Column(db.Integer, db.ForeignKey("tree_node_object.id"))

    ##Datetime this was put on the queue
    time = db.Column(db.DateTime)

    ##The website to publish
    website_id = db.Column(db.Integer, db.ForeignKey("website.id"))

    ## Indicates if this errored out and is recoverable
    recoverable = db.Column(db.Boolean, default=True)

    ## Pushes an item on the queue
    # \param website the website to put in the queue
    # \param fileObject the fileObject to put in the queue
    # \note only one of the arguments needs to be given
    @classmethod
    def Push(cls, website=None, fileObject=None):
        creation = dict(
            time = datetime.datetime.now(), 
        )
        if website is not None:
            creation["website_id"] = website.id
            pass
        elif fileObject is not None:
            creation["fileObject_id"] = fileObject.id
            pass
        return cls.Create(**creation)

    ## Pops the first element off the queue 
    # \return the first object in the queue
    # \raises InvalidEntryException if fileObject_id and website_id is none
    @classmethod
    def Pop(cls):
        entry = cls.query.filter(cls.recoverable==True).order_by(cls.id).first()
        if entry is None:
            raise QueueIsEmptyException
        if entry.fileObject_id is not None:
            obj = TreeNodeObject.polyQuery().filter(TreeNodeObject.id==entry.fileObject_id).first()
            entry.delete()
            return obj
        elif entry.website_id is not None:
            obj = Website.query.get(entry.website_id)
            entry.delete()
            return obj
        entry.recoverable = False
        entry.save()
        raise InvalidEntryException

    ## checks if the queue is empty
    # \return True if the queue is empty else false
    @classmethod
    def Empty(cls):
        return cls.query.filter(cls.recoverable==True).count() <= 0





