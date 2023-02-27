import unittest
import requests
import base64
import io
import uuid
from PIL import Image, PngImagePlugin

import sys
import logging
import time

logger = logging.getLogger()
logger.level = logging.DEBUG
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

URL = "http://172.20.10.25:7720"
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}


class TestCreateModelWorking(unittest.TestCase):
    def setUp(self):
        self.url_create_model = URL+"/dreambooth/createModel"
        self.create_model = {
            "new_model_name": "api_create_model_0223_1026",
            "new_model_src": "sd-v1.5.ckpt"
        }

    def test_create_model_performed(self):
        responseCreateModel = requests.post(
            self.url_create_model, self.create_model, headers)
        self.assertEqual(responseCreateModel.status_code, 200)
        # r = responseCreateModel.json()
        # logger.info(r)


if __name__ == "__main__":
    unittest.main()
