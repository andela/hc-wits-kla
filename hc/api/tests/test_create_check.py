import json

from hc.api.models import Channel, Check
from hc.test import BaseTestCase


class CreateCheckTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(CreateCheckTestCase, self).setUp()

    def post(self, data, expected_error=None):
        r = self.client.post(self.URL, json.dumps(data),
                             content_type="application/json")

        if expected_error:
            self.assertEqual(r.status_code, 400)
            ### Assert that the expected error is the response error

        return r

    def test_it_works(self):
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })

        self.assertEqual(r.status_code, 201)

        doc = r.json()
        self.assertIn("ping_url", doc)
        self.assertEqual("Foo", doc["name"])
        self.assertEqual("bar,baz", doc["tags"])

        ### Assert the expected last_ping and n_pings values
        self.assertEqual(0, doc['n_pings'])
        self.assertEqual(None, doc['last_ping'])

        self.assertEqual(Check.objects.count(), 1)
        check = Check.objects.get()
        self.assertEqual("Foo", check.name)
        self.assertEqual("bar,baz", check.tags)
        self.assertEqual(3600, check.timeout.total_seconds())
        self.assertEqual(60, check.grace.total_seconds())

    def test_it_accepts_api_key_in_header(self):
        payload = json.dumps({"name": "Foo"})

        ### Make the post request and get the response
        r = self.client.post(self.URL, payload, content_type="application/json", HTTP_X_API_KEY="abc")
        self.assertEqual(201, r.status_code)

    def test_it_handles_missing_request_body(self):
        ### Make the post request with a missing body and get the response
        expected_result = {'status_code': 400, 'error': "wrong api_key"} ### This is just a placeholder variable
        r = self.client.post(self.URL, content_type="application/json")
        r_to_json = r.json()

        self.assertEqual(400, r.status_code)
        self.assertEqual("wrong api_key", r_to_json["error"])

    def test_it_handles_invalid_json(self):
        ### Make the post request with invalid json data type
        payload = "a string is not json "
        expected_result = {'status_code': 400, 'error': "could not parse request body"} ### This is just a placeholder variable
        r = self.client.post(self.URL, payload, content_type="application/json")
        r_to_json = r.json()

        self.assertEqual(400, r.status_code)
        self.assertEqual("could not parse request body", r_to_json["error"])

    def test_it_rejects_wrong_api_key(self):
        self.post({"api_key": "wrong"},
                  expected_error="wrong api_key")

    def test_it_rejects_non_number_timeout(self):
        self.post({"api_key": "abc", "timeout": "oops"},
                  expected_error="timeout is not a number")

    def test_it_rejects_non_string_name(self):
        self.post({"api_key": "abc", "name": False},
                  expected_error="name is not a string")

    ### Test for the assignment of channels
    def test_it_assigns_channels(self):
        r = self.post({
            "api_key": "abc",
            "channel": "*"
        })

        self.assertEqual(201, r.status_code)

    ### Test for the 'timeout is too small' and 'timeout is too large' errors
    def test_its_timeout_too_large(self):
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 874500,
            "grace": 60
        })

        self.assertEqual(400, r.status_code)

    def test_its_timeout_too_small(self):
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 58,
            "grace": 60
        })

        self.assertEqual(400, r.status_code)
