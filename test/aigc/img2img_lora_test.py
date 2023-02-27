import base64
import io
import uuid
import io

import unittest
import requests
from gradio.processing_utils import encode_pil_to_base64
from PIL import Image, PngImagePlugin

import sys
import logging
import time
import random
import datetime
time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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


# para_prompt_txt=sys.argv[1]
para_webui_port = sys.argv[1]
para_output_dir = sys.argv[2]
para_prompt_lora = "wubing"
para_prompt_name = sys.argv[4]


print(time, f":sys.argv[0] ")


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


class TestImg2ImgWorking(unittest.TestCase):
    def setUp(self):
        self.url_img2img = f"http://localhost:{para_webui_port}/sdapi/v1/img2img"
        self.url_pnginfo = f"http://localhost:{para_webui_port}/sdapi/v1/png-info"
        self.simple_img2img = {
            # init指定模特的照片
            "init_images": [encode_pil_to_base64(Image.open(r"files/model/male.jpg"))],
            "resize_mode": 0,
            "denoising_strength": 0.75,
            "mask": None,
            "mask_blur": 4,
            "inpainting_fill": 0,
            "inpaint_full_res": False,
            "inpaint_full_res_padding": 0,
            "inpainting_mask_invert": False,
            "prompt": f"{para_prompt_name}, ID photo , portrait photo, (White background),Detailed face, 8k, profile picture, stoic facial expression, looking at the camera, photorealistic photograph cinematic lighting intricate, Ultra photoreal, Ultra detailed, Octane render, Cinematic, Full-Body Shot, HD, Full HD, 8k, <lora:{para_prompt_lora}:0.8> ",
            "styles": [],
            "seed": 4269255511,
            "subseed": -1,
            "subseed_strength": 0,
            "seed_resize_from_h": -1,
            "seed_resize_from_w": -1,
            "batch_size": 16,
            "n_iter": 1,
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

    # def test_img2img_simple_performed(self):
    #    self.assertEqual(requests.post(self.url_img2img, json=self.simple_img2img).status_code, 200)

    # def test_inpainting_masked_performed(self):
    #    self.simple_img2img["mask"] = encode_pil_to_base64(Image.open(r"test/test_files/mask_basic.png"))
    #    self.assertEqual(requests.post(self.url_img2img, json=self.simple_img2img).status_code, 200)

    # def test_inpainting_with_inverted_masked_performed(self):
    #    self.simple_img2img["mask"] = encode_pil_to_base64(Image.open(r"test/test_files/mask_basic.png"))
    #    self.simple_img2img["inpainting_mask_invert"] = True
    #    self.assertEqual(requests.post(self.url_img2img, json=self.simple_img2img).status_code, 200)

    # def test_img2img_sd_upscale_performed(self):
    #    self.simple_img2img["script_name"] = "sd upscale"
    #    self.simple_img2img["script_args"] = ["", 8, "Lanczos", 2.0]

    #    self.assertEqual(requests.post(self.url_img2img, json=self.simple_img2img).status_code, 200)

    @repeat()
    def test_img2img_simple_performed(self):
        responseImg2img = requests.post(self.url_img2img,
                                        json=self.simple_img2img)
        self.assertEqual(responseImg2img.status_code, 200)
        r = responseImg2img.json()
        self.save_image(r['images'])

    def save_image(self, images):
        for i in images:
            print(type(i))
            png_payload = {
                "image": "data:image/png;base64," + i
            }
            pngInfo = PngImagePlugin.PngInfo()
            pngInfo.add_text("parameters", requests.post(
                self.url_pnginfo, json=png_payload).json().get("info"))

            pngInfo.add_text("parameters", requests.post(
                self.url_pnginfo, json=png_payload).json().get("info"))
            # uuid_str = uuid.uuid4()
            name_id = random.randint(10, 99)
            image = Image.open(io.BytesIO(
                base64.b64decode(i.split(",", 1)[0])))
            image.save(
                f'{para_output_dir}/{name_id}_ai_img2img.png', pnginfo=pngInfo)
            # image.save(f'./images/{name_id}ai_pic.png')
            # 图片保存
        sys.exit(0)


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
