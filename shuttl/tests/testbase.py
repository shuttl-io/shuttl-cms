import os
import unittest
from flask.ext.migrate import upgrade, migrate
import sqlalchemy

import shuttl
from shuttl.settings import TestConfig, LocalTestConfig
from shuttl.Models.Reseller import Reseller


class BaseTest(unittest.TestCase):
    def setUp(self):
        try:
            klass = TestConfig
            if os.environ.get('SHUTTL_LOCAL'):
                klass = LocalTestConfig
                pass
            shuttl.app.config.from_object(klass)
            self.app = shuttl.app.test_client()
            self.app.allow_subdomain_redirects = True
            try:
                self.reseller = Reseller(name="shuttl", _url="shuttl.com")
                self.reseller.save()
            except:
                shuttl.db.session.rollback()
                self.reseller = Reseller.query.filter(Reseller.name == "shuttl").first()
                if self.reseller is None:
                    self.reseller = Reseller(name="shuttl", _url="shuttl.com")
                    self.reseller.save()
                    pass
                pass
            try:
                self._setUp()
                pass
            except:
                shuttl.db.session.rollback()
                self.tearDown()
                raise
            pass
        except:
            shuttl.db.session.rollback()
            self.tearDown()
            self._setUp()
        pass

    def removeWhiteSpace(self, str):
        return "".join(str.split())

    def _getSubdomain(self):
        return None

    def _setUp(self):
        pass

    def _tearDown(self):
        pass

    def tearDown(self):
        try:
            BaseTest.clear_data(shuttl.db.session)
            pass
        except sqlalchemy.orm.exc.StaleDataError:
            pass
        shuttl.db.session.remove()
        self._tearDown()
        pass

    @classmethod
    def clear_data(cls, session):
        meta = shuttl.db.metadata
        tableName = []
        for table in reversed(meta.sorted_tables):
            tableName.append("\"{0}\"".format(table.name))
            pass
        tableNames = ", ".join(tableName)

        session.execute("TRUNCATE TABLE {0} RESTART IDENTITY CASCADE".format(tableNames))
        session.commit()
        pass
