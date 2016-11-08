import os
from git import Repo
import tempfile
import uuid
import datetime

from .Base import BasePublisher
from shuttl.database import db
from shuttl.Storage import Storage

class S3Publisher(BasePublisher):

    ##Id of the directory. Because of the way inheritance is set up in sqlalchemy, this is a foriegnKey
    id = db.Column(db.Integer, db.ForeignKey('base_publisher.id'), primary_key=True)

    bucketName = db.Column(db.String, nullable=False)

    protocol = "s3"

    __mapper_args__ = {
        'polymorphic_identity':'s3_publisher',
    }

    def save(self, *args, **kwargs):
        self.bucketName = self.name.lower().replace("_")


    def createBucketName(self, name, count=0):
        name = "".join([name, str(count)]) if count != 0 else name
        if S3Publisher.query.filter(S3Publisher.bucketName==name).first() is not None:
            return self.createBucketName(name, count+1)
        return name

    ## Sets up the connection to the remote server
    def _setUpConnection(self):
        acl = "public-read"
        self.bucket = Storage(self.bucketName, acl, siteOptions=dict(ErrorDocument="/base.html"))
        pass

    ## Publishes a fileObject (required)
    # \param file the file to publish
    def publishFile(self, file):
        filePath = file.fullPath[1:]
        filePath = os.path.join(self.baseDir, filePath)
        with open(filePath, "wb+") as fi:
            content = file.buildContent(
                website=file.website, 
                page=file, 
                organization=file.website.organization, 
                publisher=self
            )
            if type(content) == str:
                content = content.encode()
                pass
            fi.write(content)
            pass
        s3_path = self.getPath(file.fullPath)[1:]
        kwargs = dict(
            hostPath=s3_path, 
            filePath=filePath, 
            mimeType=file.headers().get("Content-Type", "text/plain")
        )
        self.bucket.upload(**kwargs)
        pass

    ## Publishes a directory before the files (optional)
    # \param object the object to publish
    def publishDirectory(self, directory):
        dirPath = directory.fullPath[1:]
        dirPath = os.path.join(self.baseDir, dirPath)
        try:
            os.mkdir(dirPath)
            pass
        except FileExistsError:
            #the directory already exsists. Let's just ignore this.
            pass
        pass