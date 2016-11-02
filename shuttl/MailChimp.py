import requests
from requests.auth import HTTPBasicAuth
import os

from shuttl import app


class MailChimpError(Exception): pass

class MailChimp:

    token = app.config["MAILCHIMP_TOKEN"]
    url = app.config["MAILCHIMP_URL"]

    @classmethod
    def AddUserToList(cls, emailAdress, first_name, last_name):
        if app.config["TESTING"] or app.config["DEBUG"]:
            return
        url = os.path.join(cls.url, "lists/2892f34576/members/")
        data = dict(
            email_address=emailAdress,
            merge_fields=dict(
                FNAME=first_name,
                LNAME=last_name
            ),
            status="subscribed"
        )
        auth = HTTPBasicAuth('anystring', cls.token)
        res = requests.post(url, auth=auth, json=data)
        if res.status_code >= 200 or res.status_code <= 399 :
            return res.json()
        raise MailChimpError("Failed with status code: {0}".format(res.status_code))