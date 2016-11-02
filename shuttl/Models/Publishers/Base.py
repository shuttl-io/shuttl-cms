from shuttl import app
from shuttl.database import BaseModel, db
from shuttl.Templates.Tags import load_tags

class BasePublisher(BaseModel, db.Model):

    protocol = "N/A"

    ## Id of the publisher
    id = db.Column(db.Integer, primary_key=True)

    ##The name of the publisher
    name = db.Column(db.String, nullable=False)

    ## relative URL of the publisher. EG: the root directory
    relativeUrl = db.Column(db.String, default="/", nullable=False)

    ##The hostname to publish to
    hostname = db.Column(db.String, nullable=False)

    ##The id of the website that this publisher belongs to
    website_id = db.Column(db.Integer, db.ForeignKey('website.id'))

    ## The actuall Website object that owns this publisher
    website = db.relationship("Website", foreign_keys=[website_id], back_populates='publishers')

    type = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity':'base_publisher',
        'polymorphic_on':type,
        "with_polymorphic": "*"
    }


    ## Publishes a fileObject (required)
    # \param object the object to publish
    def publishFile(self, object):
        raise NotImplementedError

    ## Publishes a directory before the files (optional)
    # \param object the object to publish
    def publishDirectory(self, object):
        pass

    def setUpConnection(self):
        load_tags(app.jinja_env)
        return self._setUpConnection()

    ## Sets up the connection to the remote server
    def _setUpConnection(self):
        raise NotImplementedError

    ## Destroys the connection
    def destroyConnection(self):
        pass

class BaseMock(BasePublisher):
    id = db.Column(db.Integer, db.ForeignKey('base_publisher.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'publish_mock',
    }

    fileCount = 0
    dirCount = 0

    def publishFile(self, object):
        self.fileCount += 1
        pass

    def publishDirectory(self, object):
        self.dirCount += 1
        pass
