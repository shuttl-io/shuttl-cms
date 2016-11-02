from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]

from shuttl.Models.organization import Organization, OrganizationDoesNotExistException
from urllib.parse import urlparse, urlunparse
from flask import redirect

##Add subdomain to request to allow for switching to specific domains
# \param location location relative to the app root that you're redirecting to
# \url url that the subdomain is being added to
# \subdomain the subdomain that is being added to the url
def redirect_subdomain(location, url, subdomain):
    try:
        org = Organization.Get(name=subdomain)
    except OrganizationDoesNotExistException:
        raise OrganizationDoesNotExistException
    urlparts = urlparse(url)
    urlparts_list = list(urlparts)
    urlparts_list[1] = subdomain + '.' + urlparts_list[1]
    urlparts_list[2] = location

    return redirect(urlunparse(urlparts_list))