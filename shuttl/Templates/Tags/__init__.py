from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]

from .WysiwygTag import *
from .FileTag import *
from .TextTag import *
from .TextTag import *
from .SiteMapTag import SiteMapExtension
from .IncludeTag import ObtainTagExtension
from .ForEach import ForEachTag
from .Base import BaseTagExtension

## loads all tags.
# \param jinja_env the env to add the tags to
def load_tags(jinja_env):
    for i in BaseTagExtension.__subclasses__():
        jinja_env.add_extension(i)
        pass
    pass
