import argparse
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
        self.url_txt2img = URL+"/sdapi/v1/txt2img"
        self.url_pnginfo = URL+"/sdapi/v1/png-info"
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
            image.save(f'512/{c}{uuid_str}.png', pnginfo=pngInfo)
            index += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--p', default='7720')
    parser.add_argument('--c', default='0')
    parser.add_argument('unittest_args', nargs='*')

    args = parser.parse_args()
    c = args.c
    URL = "http://172.20.10.25:"+args.p

    # Now set the sys.argv to the unittest_args (leaving sys.argv[0] alone)
    sys.argv[1:] = args.unittest_args

    fh = logging.FileHandler(f"logs/{c}/txt2img.log")
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    unittest.main()
