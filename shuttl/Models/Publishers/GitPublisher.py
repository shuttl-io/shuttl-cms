import os
from git import Repo
import tempfile
import uuid
import datetime

from .Base import BasePublisher
from shuttl.database import db

class GitPublisher(BasePublisher):

    ##Id of the directory. Because of the way inheritance is set up in sqlalchemy, this is a foriegnKey
    id = db.Column(db.Integer, db.ForeignKey('base_publisher.id'), primary_key=True)

    protocol = "GIT"

    privateKeyPath = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity':'git_publisher',
    }

    ## Sets up the connection to the remote server
    def _setUpConnection(self):
        jobID = str(uuid.uuid4())
        self.baseDir = os.path.join("/tmp/", jobID)
        os.mkdir(self.baseDir)
        id_file = os.path.expanduser(self.privateKeyPath)
        self.ssh_cmd = 'ssh -i %s' % id_file
        self.repo = Repo.init(self.baseDir)
        with self.repo.git.custom_environment(GIT_SSH_COMMAND=self.ssh_cmd):
            self.origin = self.repo.create_remote('origin', self.hostname)
            self.origin.fetch() 
            self.repo.create_head('master', self.origin.refs.master).set_tracking_branch(self.origin.refs.master)
            pass
        pass

    @property
    def publicKey(self):
        path = os.path.expanduser("{0}.pub".format(self.privateKeyPath))
        content = ""
        with file(path, "r") as fi:
            content = fi.read()
            pass
        return content
    
    ## Destroys the connection
    def destroyConnection(self):
        self.repo.index.commit("Published from Shuttl on {0}".format(datetime.datetime.now()))
        with self.repo.git.custom_environment(GIT_SSH_COMMAND=self.ssh_cmd):
            self.origin.push(force=True)
            pass
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
        self.repo.index.add([filePath])

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