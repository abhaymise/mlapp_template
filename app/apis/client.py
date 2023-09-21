#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module desciption: 
Description of what client.py does.
"""
# client.py created at 11-02-2023
import requests
from requests_toolbelt import MultipartEncoder

app_name = 'ml_inference_server'


def ping_server():
    api_end_point = "http://localhost:8888/"
    data = []
    response = requests.get(api_end_point)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"server could n't be reached ...")


def upload_image_as_bytearray(image_location):
    api_end_point = f"http://localhost:8888/{app_name}/get_prediction/"
    data = []
    image_bytearray = b''
    fields = []
    fields.append(('image', image_bytearray, 'image/jpeg'))
    payload = MultipartEncoder(fields)
    content_type = payload.content_type
    header = {'content-type': content_type}
    try:
        response = requests.post(api_end_point, data=fields, headers=header)
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"upload failed ...")
    except requests.exceptions.HTTPError as e:
        print(e.response.text)
    return data


if __name__ == '__main__':
    ping_server()
