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
import json

logger = logging.getLogger()
logger.level = logging.DEBUG
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

URL = "http://172.20.10.25:7720"
# URL = "http://127.0.0.1:50000"
# headers = {
#     "Content-Type": "application/json; charset=UTF-8"
# }


class TestConfigModelWorking(unittest.TestCase):
    def setUp(self):
        self.url_config_model = URL+"/dreambooth/concept?model_name="
        self.config_model_name = 'api_create_model_0223_1026'
        self.config_model_data = "/data/zhangying"
        self.config_model = {
            "concept": {
                "class_data_dir": "",
                "class_guidance_scale": 7.5,
                "class_infer_steps": 60,
                "class_negative_prompt": "",
                "class_prompt": "",
                "class_token": "",
                "instance_data_dir": "/data/zhangying",
                "instance_prompt": "",
                "instance_token": "",
                "is_valid": False,
                "n_save_sample": 1,
                "num_class_images": 0,
                "num_class_images_per": 0,
                "sample_seed": -1,
                "save_guidance_scale": 7.5,
                "save_infer_steps": 60,
                "save_sample_negative_prompt": "",
                "save_sample_prompt": "",
                "save_sample_template": ""
            }
        }

    def test_config_model_performed(self):
        responseCreateModel = requests.post(
            self.url_config_model+self.config_model_name+"&instance_dir="+self.config_model_data,  json=self.config_model)
        r = responseCreateModel.json()
        logger.info(r)
        self.assertEqual(responseCreateModel.status_code, 200)


if __name__ == "__main__":
    unittest.main()
