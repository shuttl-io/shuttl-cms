from shuttl.Models.Queue import Queue

from werkzeug.datastructures import FileStorage
from flask.ext.script.commands import Command
from shuttl.tests.testbase import BaseTest
import shuttl
import os

class ResetPublishers(Command):

    def run(self):
        for i in Queue.query.all():
            i.recoverable = True
            i.save()
            pass
