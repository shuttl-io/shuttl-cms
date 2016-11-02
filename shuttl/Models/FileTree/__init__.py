from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]

from .FileObjects import *
import os
fileTypes = dict()

for cls in FileObject.FileObject.__subclasses__():
    if "mock" not in cls.__name__.lower():
        fileTypes[cls.fileExt] = cls
        pass

## Gets the file class type from an uploaded file
# \param file the FileStorage object that was uploaded
# \return the class that this file should be associated with
def get_upload_file_class(file):
    _, extension = os.path.splitext(file.filename)
    extension = extension.replace(".", "")
    cls = fileTypes.get(extension)
    if cls is None:
        return FileObject.FileObject
    return cls