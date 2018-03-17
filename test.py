import os
import unittest
import json
from app import app
import logging

TEST_DB = 'test.db'

logging.basicConfig(filename='testing-logs.log', level=logging.DEBUG,format='[%(levelname)s]: [%(asctime)s] [%(message)s]', datefmt='%m/%d/%Y %I:%M:%S %p')

class TestOfConfigAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()


    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        logging.info(("health check is done - working"))
        self.assertEqual(response.status_code, 200)

    def test_get_method_config(self):
        response = self.app.get('/config?tenant=hello&integration_type=hello', follow_redirects=True)
        logging.info(("/config get method is done - working"))
        self.assertEqual(response.status_code, 200)
    def test_post_method_config(self):
        response = self.app.post('/config', data = json.dumps('{"tenant": "tata","integration_type": "byee","configuration": {"username": "ujyfjhgkgk","password": "dc","wsdl_urls": {"session_url": "scs","booking_url": "sd123"}}}'))
        logging.info(("/config post method is done - working"))
        self.assertEqual(response.status_code, 200)
    def test_get_method_config_error(self):
        response = self.app.get('/config?integration_type=hello', follow_redirects=True)
        logging.info(("/config get method is done - woring"))
        self.assertEqual(response.status_code, 200)
    def test_post_method_config_error(self):
        response = self.app.post('/config', data = json.dumps('{"integration_type": "byee","configuration": {"username": "ujyfjhgkgk","password": "dc","wsdl_urls": {"session_url": "scs","booking_url": "sd123"}}}'))
        logging.info(("/config post method is done - working"))
        self.assertEqual(response.status_code, 200)
if __name__ == "__main__":
    unittest.main()