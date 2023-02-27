import unittest
import requests
import base64
import io
# import uuid
from PIL import Image, PngImagePlugin

import sys
import logging
import time
import argparse

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


def encode_pil_to_base64(image):
    with io.BytesIO() as output_bytes:
        use_metadata = False
        metadata = PngImagePlugin.PngInfo()
        for key, value in image.info.items():
            if isinstance(key, str) and isinstance(value, str):
                metadata.add_text(key, value)
                use_metadata = True
            image.save(output_bytes, format="PNG", pnginfo=(
                metadata if use_metadata else None), quality=80)
        bytes_data = output_bytes.getvalue()

    base64.b64encode(bytes_data)
    base64_str = str(base64.b64encode(bytes_data), "utf-8")
    return "data:image/png;base64," + base64_str


class TestImg2ImgWorking(unittest.TestCase):

    def setUp(self):
        self.url_img2img = URL+"/sdapi/v1/img2img"
        self.url_pnginfo = URL+"/sdapi/v1/png-info"
        self.url_sd_models = URL+"/sdapi/v1/sd-models"
        self.options = URL+"/sdapi/v1/options"
        self.refresh = URL+"/sdapi/v1/refresh-checkpoints"
        init_images = []
        init_images.append(encode_pil_to_base64(
            Image.open(r"%s" % (img))))

        self.simple_img2img = {
            # init指定模特的照片
            "init_images": init_images,
            "resize_mode": 0,
            "denoising_strength": 0.75,
            "mask": None,
            "mask_blur": 4,
            "inpainting_fill": 0,
            "inpaint_full_res": False,
            "inpaint_full_res_padding": 0,
            "inpainting_mask_invert": False,
            "prompt": f"wubing, ID photo , portrait photo, (White background),Detailed face, 8k, profile picture, stoic facial expression, looking at the camera, photorealistic photograph cinematic lighting intricate, Ultra photoreal, Ultra detailed, Octane render, Cinematic, Full-Body Shot, HD, Full HD, 8k, <lora:{para_prompt_lora}:0.8> ",
            "styles": [],
            "seed": 4269255511,
            "subseed": -1,
            "subseed_strength": 0,
            "seed_resize_from_h": -1,
            "seed_resize_from_w": -1,
            "batch_size": 6,
            "n_iter": 3,
            "steps": 50,
            "cfg_scale": 2,
            "width": 512,
            "height": 512,
            "restore_faces": True,
            "tiling": False,
            "negative_prompt": "nsfw letterbox,gape60_fix3,(bad_prompt:0.8) bad anatomy, bad perspective, multiple views, concept art, reference sheet, mutated hands and fingers, interlocked fingers, twisted fingers, excessively bent fingers, more than five fingers, lowres, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name, low quality lowres multiple breasts, low quality lowres mutated hands and fingers, more than two arms, more than two hands, more than two legs, more than two feet, low quality lowres long body, low quality lowres mutation poorly drawn, low quality lowres black-white, low quality lowres bad anatomy",
            "eta": 0,
            "s_churn": 0,
            "s_tmax": 0,
            "s_tmin": 0,
            "s_noise": 1,
            "override_settings": {},
            "sampler_index": "Euler a",
            "include_init_images": False
        }
        # responseRefresh = requests.post(self.refresh)
        # self.assertEqual(responseRefresh.status_code, 200)

        responseSdModels = requests.get(self.url_sd_models)
        self.assertEqual(responseSdModels.status_code, 200)

        sdModels = responseSdModels.json()
        for m in sdModels:
            logger.info(m["title"])
        options = {
            "sd_model_checkpoint": "Midjourney-v4.ckpt [5d5ad06cc2]",
        }
        logger.info("select model => "+options["sd_model_checkpoint"])
        responseOptions = requests.post(self.options, json=options)
        self.assertEqual(responseOptions.status_code, 200)

    @repeat()
    def test_img2img_simple_performed(self):
        responseTxt2img = requests.post(self.url_img2img,
                                        json=self.simple_img2img)
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
    parser.add_argument('--i', default="female.jpg")
    parser.add_argument('--c', default='0')
    parser.add_argument('unittest_args', nargs='*')
    args = parser.parse_args()

    URL = "http://localhost:"+args.p
    img = args.i
    c = args.c
    para_prompt_lora = "wcc4"

    fh = logging.FileHandler(f'logs/{c}/i2i.log')
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    # Now set the sys.argv to the unittest_args (leaving sys.argv[0] alone)
    sys.argv[1:] = args.unittest_args
    unittest.main()
