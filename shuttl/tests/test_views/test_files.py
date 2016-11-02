import json
import os
from werkzeug.datastructures import FileStorage
import unittest
from io import BytesIO

from shuttl import app
from shuttl.tests import testbase
from shuttl.Models.Reseller import Reseller
from shuttl.Models.organization import Organization, OrganizationDoesNotExistException
from shuttl.Models.Website import Website
from shuttl.Models.FileTree.FileObjects.FileObject import FileObject
from shuttl.Models.FileTree.Directory import Directory
from shuttl.Models.FileTree.FileObjects.CssFile import CssFile
from shuttl.Models.FileTree.TreeNodeObject import TreeNodeObject
from shuttl.Models.FileTree.FileObjects.ImageFile import ImageFile

class FilesViewTest(testbase.BaseTest):
    def _setUp(self):
        self.organization = Organization.Create(self.reseller, name="test")
        self.website = Website.Create(name="thing", organization=self.organization)
        self.dir = Directory.Create(name="Something", website=self.website)
        self.maxDiff = None
        pass

    # def _getSubdomain(self):
    #     return "test"

    def test_login(self):
        rv = self.login('test')
        pass

    def login(self, organization):
        return self.app.post('/login', data=dict(
            organization=organization
        ), follow_redirects=True)

    @unittest.skipIf(app.config["SHOULD_SKIP"], reason='fix later')
    def test_creation(self):
        results = self.app.post("http://test.shuttl.com:5000/website/1/files/css/", data=dict(name='newfile.css', parent_id=self.website.root.id, file_contents='<gimme them dank memes>'))
        self.assertEquals(results.status_code, 201)
        results2 = self.app.post("http://test.shuttl.com:5000/website/1/files/js/", data=dict(name='newfile.js', parent_id=self.website.root.id, file_contents='console.log();'))
        results3 = self.app.post("http://test.shuttl.com:5000/website/1/files/css/", data=dict(name='newfile.css', parent_id=self.website.root.id, file_contents='<gimme them dank memes>'))
        self.testFilePath = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.css")
        self.testFilePath2 = os.path.join(app.config["BASE_DIR"], "shuttl/test_files", "test.png")
        with open(self.testFilePath, 'rb') as fp:
            resultFile = self.app.post("http://test.shuttl.com:5000/website/1/files/css/", data=dict(name='realfile.css', parent_id=str(self.website.root.id), file=(fp, 'test_file.css')), content_type='multipart/form-data')
        with open(self.testFilePath2, 'rb') as fp:
            resultFile2 = self.app.post("http://test.shuttl.com:5000/website/1/files/image/", data=dict(name='realfile.png', parent_id=str(self.website.root.id), file=(fp, 'test_file.css')), content_type='multipart/form-data')
        self.assertEquals(results3.status_code, 409)
        expected = {
            'fullPath': '/newfile.css',
            'id': 5,
            'content': '<gimme them dank memes>',
            'fileType': 'css',
            'name': 'newfile.css',
            'parent': {
                'fullPath': '/',
                'id': 2,
                'children': [{
                    'fullPath': '/_hidden',
                    'id': 3,
                    'children': [],
                    'name':
                    '_hidden'
                }],
                'parent': 'None',
                'name': 'root'
            }
        }
        expected2 = {
            'fullPath': '/realfile.css',
            'parent': {
                'children': [
                    {
                        'children': [],
                        'fullPath': '/_hidden',
                        'name': '_hidden',
                        'id': 3
                    },
                    {
                        'fullPath': '/newfile.css',
                        'id': 5,
                        'content': '<gimme them dank memes>',
                        'name': 'newfile.css',
                        'fileType': 'css'
                    },
                    {
                        'fullPath': '/newfile.js',
                        'id': 6,
                        'content': 'console.log();',
                        'name': 'newfile.js',
                        'fileType': 'js'
                    }
                ],
                'fullPath': '/',
                'name': 'root',
                'id': 2,
                'parent': 'None'
            },
            'id': 8,
            'content': 'p{\n    text-align: center;\n}\n',
            'name': 'realfile.css',
            'fileType': 'css'
        }

        expected3 = {
            'fileType': 'image',
            'fullPath': '/realfile.png',
            'id': 8,
            'name': 'realfile.png',
            'parent': {
                '_children':
                    [
                        {
                            'content': '<gimme them dank memes>',
                            'fileType': 'css',
                            'fullPath': '/newfile.css',
                            'id': 4,
                            'name': 'newfile.css'
                        },
                        {
                            'content': 'console.log();',
                            'fileType': 'js',
                            'fullPath': '/newfile.js',
                            'id': 5,
                            'name': 'newfile.js'
                        },
                        {
                            'content': 'p{\n    text-align: center;\n}\n',
                            'fileType': 'css',
                            'fullPath': '/realfile.css',
                            'id': 7,
                            'name': 'realfile.css'
                        }
                    ],
                'fullPath': '/',
                'id': 2,
                'name': 'root',
                'parent': 'None'
            },
        }


        self.assertEquals(expected, json.loads(results.data.decode()))
        res = json.loads(resultFile.data.decode())
        self.assertEquals(expected2, res)
        self.assertEquals(len(CssFile.query.all()), 2)
        self.assertEquals(len(TreeNodeObject.query.all()), 7)
        pass
    @unittest.skipIf(app.config["SHOULD_SKIP"], reason='fix later')
    def test_getAll(self):
        results = self.app.post("http://test.shuttl.com:5000/website/1/files/css/", data=dict(name='newfile.css', parent_id=self.website.root.id, file_contents='<gimme them dank memes>'))
        results = self.app.post("http://test.shuttl.com:5000/website/1/files/js/", data=dict(name='newfile.js', parent_id=self.website.root.id, file_contents='<gimme them dank memes>'))
        filesList = self.app.get("http://test.shuttl.com:5000/website/1/files/")
        pass
    @unittest.skipIf(app.config["SHOULD_SKIP"], reason='fix later')
    def test_get(self):
        results = self.app.post("http://test.shuttl.com:5000/website/1/files/css/", data=dict(name='newfile.css', parent_id=self.website.root.id, file_contents='<gimme them dank memes>'))
        file = self.app.get("http://test.shuttl.com:5000/website/1/files/css/4/")

        expected = {
            'content': '<gimme them dank memes>',
            'id': 5,
            'fileType': 'css',
            'parent': {
                'parent': 'None',
                'children': [{
                    'children': [],
                    'fullPath': '/_hidden',
                    'id': 3,
                    'name': '_hidden'
                }],
                'fullPath': '/',
                'id': 2,
                'name': 'root'
            },
            'fullPath': '/newfile.css',
            'name': 'newfile.css'
        }
        res = json.loads(results.data.decode())
        self.assertEquals(expected, res)
        pass

    @unittest.skipIf(app.config["SHOULD_SKIP"], reason='fix later')
    def test_patch(self):
        results = self.app.post("http://test.shuttl.com:5000/website/1/files/css/",
            data=dict(
                name='newfile.css',
                parent_id=self.website.root.id,
                file_contents='<gimme them dank memes>'
            )
        )
        jsonData = json.dumps(dict(
                name='renamefile.css',
                file_contents=dict(
                    local="stuff"
                )
            )
        )
        results1 = self.app.patch("http://test.shuttl.com:5000/website/1/files/css/5/",

            data=jsonData,
            content_type='application/json'
        )
        results2 = self.app.patch("http://test.shuttl.com:5000/website/1/files/css/6/",
            data=jsonData,
            content_type='application/json'
        )

        expected = {
            'reason': 'newfile.css was modified',
            'status': 'success'
        }
        expected2 = {
            'reason': 'no css file with id 6',
            'status': 'failed'
        }
        self.assertEquals(results1.status_code, 200)
        self.assertEquals(expected, json.loads(results1.data.decode()))
        self.assertEquals(results2.status_code, 404)
        self.assertEquals(expected2, json.loads(results2.data.decode()))
        pass

    @unittest.skipIf(app.config["SHOULD_SKIP"], reason='fix later')
    def test_delete(self):
        results = self.app.post("http://test.shuttl.com:5000/website/1/files/js/", data=dict(name='newfile.css', parent_id=self.website.root.id, file_contents='<gimme them dank memes>'))
        results = self.app.delete("http://test.shuttl.com:5000/website/1/files/js/5/")
        results2 = self.app.get("http://test.shuttl.com:5000/website/1/files/js/5/")

        expected = {
            "reason": "newfile.css was deleted",
            "status": "success"
        }

        expected2 = {
            "reason": "no js file with id 5",
            "status": "failed"
        }

        self.assertEquals(results.status_code, 200)
        self.assertEquals(expected, json.loads(results.data.decode()))
        self.assertEquals(results2.status_code, 404)
        self.assertEquals(expected2, json.loads(results2.data.decode()))
        pass
