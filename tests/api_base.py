import requests

class APIBase:
    def __init__(self):
        self.url = "http://localhost:5000/"
        self.face_check_endpoint = "/v2/face_existence"
        self.evaluation_endpoint = "/v2/evaluate"

    def post(self, endpoint, data, files=None, expected_response=200):
        r = requests.post(self.url + endpoint, files=files, data=data)
        if r.status_code != expected_response:
            raise ValueError("Response is different from expectation. {0} != {1}".format(r.status_code, expected_response))
        return r