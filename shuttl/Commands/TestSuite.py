import importlib
import unittest
import os
from flask.ext.script.commands import Command, Option
import sys
import xmlrunner

from shuttl import app
from shuttl.Models.Reseller import Reseller
from shuttl.tests import *


## TestSuite for running test modules from command line
# \param Command The command that is input from command line
class TestSuite(Command):
    "Testing components of your application"

    option_list = (
        Option('-m', '--module', dest='command'),
        Option('-x', '--xml', dest='xml_file'),
    )

    def run(self, command, xml_file):
        runner = None
        if command is not None:
            module_extension = 'shuttl.tests.'
            module_name = module_extension + addPrefix(command)
            if importlib.util.find_spec(module_name):
                testsuite = unittest.defaultTestLoader.loadTestsFromName(module_name)
                pass
            else:
                app.logger.error('Invalid module: ', module_name[len(module_extension):])
                pass
            pass

        else:
            testsuite = unittest.TestLoader().discover('.')
            pass

        if xml_file is not None:
            with open(xml_file, 'wb') as output:
                runner = xmlrunner.XMLTestRunner(output=output, verbosity=1).run(testsuite)
            pass
        else:
            runner = unittest.TextTestRunner(verbosity=1).run(testsuite)
            pass
        pass

        for root, _, files in os.walk(app.config["UPLOAD_DIR"]):
            for file in files:
                path = os.path.join(root, file)
                try:
                    os.remove(path)
                    pass
                except:
                    pass
                pass
            pass
        if runner is not None:
            if len(runner.errors) + len(runner.failures) != 0:
                sys.exit(-1)
                pass
        pass


## Add prefixes to the user input command
# \param command the command that is being formatted
# \return formatted command
def addPrefix(command):
    command_parts = command.split('.')
    return "test_{0}".format('.test_'.join(command_parts))
