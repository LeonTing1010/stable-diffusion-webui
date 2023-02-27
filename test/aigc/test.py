import json

import requests

from settings import BaseConf

# #create_model
host = BaseConf().get('ai', 'host')
port = BaseConf().get('ai', 'port')
create_model = BaseConf().get('ai', 'create_model')
ai_server = f"http://{host}:{port}"
payload = {'new_model_name': 'test1', 'new_model_src': 'sd-v1.5.ckpt [e1441589a6]', 'new_model_scheduler': 'ddim', 'create_from_hub': False, 'new_model_url': '', 'new_model_token': '', 'new_model_extract_ema': False}

# req:AI CreateModel API
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}
response = requests.post(f'{ai_server}/{create_model}',payload,headers)
print(response.text)
print(response.status_code)

#配置参数

concept = BaseConf().get('ai', 'concept')
payload = {'model_name': '/data/zhangying',
           "instance_dir":"",
           "instance_token":"",
            "class_token":""
}
# payload = {'model_name': 'test1'}
# req:AI CreateModel API

headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}
response = requests.post(f'{ai_server}/{concept}',payload,headers)
print(response.text)
print(response.status_code)

# #train
# start_training = BaseConf().get('ai', 'concept')
#
# payload = {'model_name': '/data/zhangying'}
# # payload = {'model_name': 'test1'}
# # req:AI CreateModel API
#
# headers = {
#     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
# }
# response = requests.post(f'{ai_server}/{start_training}',payload,headers)
# print(response.text)
# print(response.status_code)
