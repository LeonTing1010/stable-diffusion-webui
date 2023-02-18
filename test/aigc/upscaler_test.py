import unittest
import requests
import base64
import io
import os
import uuid
# from gradio.processing_utils import encode_pil_to_base64
from PIL import Image, PngImagePlugin


class TestExtrasWorking(unittest.TestCase):
    def setUp(self):
        self.url_extras_single = "http://172.20.10.25:7720/sdapi/v1/extra-single-image"
        self.url_extras_batch = "http://172.20.10.25:7720/sdapi/v1/extra-batch-images"
        self.url_pnginfo = "http://172.20.10.25:7720/sdapi/v1/png-info"

        self.extras_single = {
            "resize_mode": 1,
            "show_extras_results": True,
            "gfpgan_visibility": 0,
            "codeformer_visibility": 0,
            "codeformer_weight": 0,
            "upscaling_resize": 2,
            "upscaling_resize_w": 4096,
            "upscaling_resize_h": 4096,
            "upscaling_crop": True,
            "upscaler_1": "ESRGAN_4x",
            "upscaler_2": "None",
            "extras_upscaler_2_visibility": 0,
            "image": None
        }
        self.extras_batch = {
            "resize_mode": 1,
            "show_extras_results": True,
            "gfpgan_visibility": 0,
            "codeformer_visibility": 0,
            "codeformer_weight": 0,
            "upscaling_resize": 2,
            "upscaling_resize_w": 4096,
            "upscaling_resize_h": 4096,
            "upscaling_crop": True,
            "upscaler_1": "ESRGAN_4x",
            "upscaler_2": "None",
            "extras_upscaler_2_visibility": 0,
            "imageList": None
        }

    def test_batch_upscaling_performed(self):
        self.extras_batch['imageList'] = getAllBase64Imgfiles(
            "test/aigc/512/")
        response = requests.post(self.url_extras_batch,
                                 json=self.extras_batch)
        # print(response.json())
        self.assertEqual(response.status_code, 200)
        r = response.json()
        images = r['images']
        self.save_image(images)

    # def test_simple_upscaling_performed(self):
    #     self.extras_single['image'] = encode_pil_to_base64(Image.open(
    #         r"test/aigc/512/ff33bac8-f875-412c-83cf-677a63fbe73d.png"))
    #     response = requests.post(self.url_extras_single,
    #                              json=self.extras_single)
    #     self.assertEqual(response.status_code, 200)
    #     r = response.json()
    #     img = r['image']
    #     self.save_image([img])

    def save_image(self, images):
        for img in images:
            png_payload = {
                "image": "data:image/png;base64," + img
            }
            pngInfo = PngImagePlugin.PngInfo()
            pngInfo.add_text("parameters", requests.post(
                self.url_pnginfo, json=png_payload).json().get("info"))
            uuid_str = uuid.uuid4()
            image = Image.open(io.BytesIO(
                base64.b64decode(img.split(",", 1)[0])))
            image.save(f'test/aigc/4096/{uuid_str}.png', pnginfo=pngInfo)


def getAllBase64Imgfiles(path):
    filelist = []
    files = os.listdir(path)
    for f in files:
        absFile = os.path.join(path, f)
        if (os.path.isfile(absFile)):
            filelist.append(
                {"name": absFile, "data": encode_pil_to_base64(Image.open(absFile))})
    return filelist


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


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExtrasWorking)
    unittest.TextTestRunner(verbosity=0).run(suite)
