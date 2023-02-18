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
fh = logging.FileHandler(f'logs/512.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


def repeat():
    def repeatHelper(f):
        def callHelper(*args):
            stream_handler = logging.StreamHandler(sys.stdout)
            logger.addHandler(stream_handler)
            try:
                while True:
                    start = time.time()
                    f(*args)
                    end = time.time()
                    logging.getLogger().info(
                        "The time of execution of above program is %f s", (end-start))
            finally:
                logger.removeHandler(stream_handler)

        return callHelper

    return repeatHelper


class TestTxt2ImgWorking(unittest.TestCase):
    def setUp(self):
        self.url_txt2img = "http://localhost:7720/sdapi/v1/txt2img"
        self.url_pnginfo = "http://localhost:7720/sdapi/v1/png-info"
        self.simple_txt2img = {
            "enable_hr": False,
            "denoising_strength": 0,
            "firstphase_width": 0,
            "firstphase_height": 0,
            "prompt": "A stunning portrait headshot of a beautiful and captivating young woman with a playful and whimsical expression, centered, looking to the viewer, captured in a soft and natural lighting mode with a dreamy and romantic atmosphere reminiscent of the film Amélie, showcasing the subject's beauty and charm in a vibrant and colorful style at a high resolution",
            "styles": [],
            "seed": -1,
            "subseed": -1,
            "subseed_strength": 0,
            "seed_resize_from_h": -1,
            "seed_resize_from_w": -1,
            "batch_size": 16,
            "n_iter": 1,
            "steps": 50,
            "cfg_scale": 7,
            "width": 512,
            "height": 512,
            "restore_faces": False,
            "tiling": False,
            "negative_prompt": "distorted, bad anatomy, weird, ugly, blurry, bad anatomy, distorted, disfigured, ((poorly drawn hands)), ((poorly drawn face)), (((disfigured))), out of frame, ugly, extra limbs, (bad anatomy), gross proportions, (malformed limbs), letter",
            "eta": 0,
            "s_churn": 0,
            "s_tmax": 0,
            "s_tmin": 0,
            "s_noise": 1,
            "sampler_index": "Euler a"
        }

    @repeat()
    def test_txt2img_simple_performed(self):
        responseTxt2img = requests.post(self.url_txt2img,
                                        json=self.simple_txt2img)
        self.assertEqual(responseTxt2img.status_code, 200)
        r = responseTxt2img.json()
        self.save_image(r['images'])

    def save_image(self, images):
        index = 1
        for i in images:
            png_payload = {
                "image": "data:image/png;base64," + i
            }
            pngInfo = PngImagePlugin.PngInfo()
            pngInfo.add_text("parameters", requests.post(
                self.url_pnginfo, json=png_payload).json().get("info"))
            uuid_str = str(index)
            image = Image.open(io.BytesIO(
                base64.b64decode(i.split(",", 1)[0])))
            image.save(f'512/{uuid_str}.png', pnginfo=pngInfo)
            index += 1


if __name__ == "__main__":
    unittest.main()
