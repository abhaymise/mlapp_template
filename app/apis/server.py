#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module desciption: 
Description of what server.py does.
"""
# server.py created at 11-02-2023

import json
import time
from enum import Enum
from pathlib import Path

import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse


class ProcessStatus(Enum):
    PASSED = 1
    FAILED = -1
    IN_PROGRESS = 0


app = FastAPI()
app_name = "ml_inference_server"

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time.perf_counter()
        result = func(*args, **kwargs)
        t2 = time.perf_counter()
        total_time = (t2 - t1)
        print(f'Function {func.__name__!r} executed in {total_time * 1000:.4f} milliseconds')
        return result

    return wrap_func


@app.get("/")
def whoami():
    return f" hi am {app_name} app "


@app.get("/health")
def health():
    return {"status": "ok"}


def parse_request(raw_request):
    pass


@app.post(f"{app_name}/upload/image")
async def upload_image(request: Request):
    upload_dir = "static"
    Path(upload_dir).mkdir(exist_ok=True, parents=True)
    image_name = "test"
    ext = ".jpeg"
    image_path = f"{upload_dir}/{image_name}{ext}"
    # image_array = read_image_from_request(request)
    whole_byte_array = b''
    async for byte_block in request.stream():
        whole_byte_array += byte_block
    image_array = np.fromstring(whole_byte_array, np.uint8)
    image_array = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    print(f"image saved at {image_path}")
    cv2.imwrite(image_path, image_array)
    return {"message": "sucess", "image_path": image_path}


@timer_func
@app.post(f'{app_name}/get_prediction/', response_class=ORJSONResponse)
async def get_prediction(image: UploadFile = File(...)):
    response = {
        'data': [],
        'status': "",
        "message": ""
    }
    file_name = image.filename
    image_reader = await image.read()  # bytearray
    image_one_d_array = np.frombuffer(image_reader, np.uint8)
    image_bgr_array = cv2.imdecode(image_one_d_array, cv2.IMREAD_COLOR)
    image_rgb_array = image_bgr_array[..., ::-1]
    # score_array = predict_proba(image_rgb_array,threshold=0.5)
    data = {'file_name': file_name,
            "label": "",
            "conf": 0.0
            }
    response['data'] = data
    response['status'] = ProcessStatus.PASSED.name
    json_string = json.dumps(response)
    return json_string


def start_server():
    # uvicorn.run(app, port=8888, host="0.0.0.0")  # ,reload=True, debug=True)
    uvicorn.run(f"{Path(__file__).stem}:app", port=8888, host="0.0.0.0", log_level="info", reload=True)  # , debug=True)


def main():
    start_server()


if __name__ == '__main__':
    main()
