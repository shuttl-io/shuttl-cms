from flask.ext.script.commands import Command

from shuttl.Storage import Storage
from shuttl.Models.FileTree.FileObjects.FileObject import FileObject

class UploadS3(Command):
    "Filling the Database with mock info"

    def run(self):
        for fi in FileObject.polyQuery().all():
            Storage.Upload(fi)
            pass
        pass