import unittest
import requests
import base64
import io
import uuid
from PIL import Image, PngImagePlugin
from urllib import parse
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


class TestConfigModelWorking(unittest.TestCase):
    def setUp(self):
        self.url_config_model = URL+"/dreambooth/model_params"
        self.config_model = {'model_name': 'api_create_model_0222_1612',
                             'params': '{"instance_data_dir": "/data/zhangying"}'}

    def test_config_model_performed(self):
        responseCreateModel = requests.post(
            self.url_config_model, self.config_model, headers=headers)
        r = responseCreateModel.json()
        logger.info(r)
        self.assertEqual(responseCreateModel.status_code, 200)


if __name__ == "__main__":
    unittest.main()
