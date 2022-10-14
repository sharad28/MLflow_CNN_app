import imghdr
import os
from tkinter import Image
import yaml
import logging
import time
import pandas as pd
import json

def read_yaml(path_to_yaml: str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    logging.info(f"yaml file: {path_to_yaml} loaded successfully")
    return content

def create_directories(path_to_directories: list) -> None:
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        logging.info(f"created directory at: {path}")


def save_json(path: str, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logging.info(f"json file saved at: {path}")

def validate_img(img_full_path):
    try:
        logging.info(f"Started verify img: {img_full_path}")
        img = Image.open(img_full_path)
        img.verify()
        if len(img.getbands()) !=3 or imghdr.what(img_full_path) not in ['jpeg','png']:
            

        logging.info(f"Completed verify img: {img_full_path}")
        return True
    except Exception as e:


def moving_data(source,destination):
    for imgs in os.listdir(source):
        if validate_img(os.path.join(source,imgs)): 


