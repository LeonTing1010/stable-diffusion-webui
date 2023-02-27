#!/bin/bash
source /home/duser/stable-diffusion-webui/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0
nohup  /home/duser/stable-diffusion-webui/venv/bin/python3 /home/duser/stable-diffusion-webui/launch.py --listen --port 7720 --api --api-log   >>  /home/duser/stable-diffusion-webui/webui0.log 2>&1 &

