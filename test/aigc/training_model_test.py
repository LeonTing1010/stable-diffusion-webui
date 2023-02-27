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
logger.level = logging.INFO
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

URL = "http://172.20.10.25:7720"
# headers = {
#     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
# }


class TestTrainingModelWorking(unittest.TestCase):
    def setUp(self):
        self.url_training_model = URL+"/dreambooth/start_training"
        self.training_model = {
            "model_name": "api_create_model_0222_1612",
            "use_tx2img": False,
        }

    # @repeat()
    def test_training_model_performed(self):
        responseCreateModel = requests.post(
            self.url_training_model, self.training_model)
        self.assertEqual(responseCreateModel.status_code, 200)
        # r = responseCreateModel.json()
        # logger.info(responseCreateModel)


if __name__ == "__main__":
    unittest.main()
