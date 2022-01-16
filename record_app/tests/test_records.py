import unittest

from flask.json.tag import JSONTag
from main import create_app
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["FLASK_ENV"] = "testing"

class TestRecords(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()


    def test_records_index(self):
        response = self.client.get("/records/")
        data = response.get_json()

    def test_create_bad_records(self):
        response = self.client.post("/records/", data={"records_name": ""})
        self.assertEqual(response.status_code, 400)

    def test_create_good_record(self):
        response = self.client.post("/records/", data={"records_name" ""})
        self.assertEqual (response.status_code, 200)
        self.assertEqual(response.get_json()["record_name"], "testrecord")
        self.client.delete(f"/records/{response.get_json()['record_id']}/")

    def test_delete_record(self):
        response1 = self.client.post("/records/", data={"record_name": "testrecord"})
        id = response1.get_json()["record_id"]
        
        response2 = self.client.delete(f"/records/{id}/")
        self.assertEqual(response2.status_code, 200)

    def test_update_record(self):
        # create the resource to test
        response1 = self.client.post("/records/", data={"record_name": "testrecord"})
        id = response1.get_json()["record_id"]

        # change the resource and check the changes were successful
        response2 = self.client.put(f"/records/{id}/", json={"record_name": "newtestrecord"})
        self.assertEqual(response2.status_code, 200)
        data = response2.get_json()
        self.assertEqual(data["record_name"], "newtestrecord")

        # clean up the resource afterwards
        self.client.delete(f"/records/{id}/")