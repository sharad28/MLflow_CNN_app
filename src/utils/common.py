import imghdr
import os
import shutil
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

# def validate_img(img_full_path,bad_img_dir):
#     try:
#         logging.info(f"Started verify img: {img_full_path}")
#         img = Image.open(img_full_path)
#         img.verify()
#         if len(img.getbands()) !=3 or imghdr.what(img_full_path) not in ['jpeg','png']:
#             bad_data_path = os.path.join(bad_img_dir, img)
#             shutil.move(img_full_path, bad_data_path)
#             continue

#         logging.info(f"Completed verify img: {img_full_path}")
#         return True
#     except Exception as e:
#         logging.exception(e)
#         raise e


def moving_data(source,destination):
    logging.info(f"Images are moving to local directory")
    try:
        for imgs in os.listdir(source):
            logging.info(f"image name{imgs} & source name {source}")
            # img_source = os.path.join(source,imgs)
            img_source = source +'\\' +imgs

            img_destin = destination[0] +'\\' +imgs
            logging.info(f"{img_source} ******* {img_destin}")
            shutil.move(img_source,img_destin) 
            logging.info(f"{img_source} is moved to local directory")
    except Exception as e:
        logging.exception(e)
        raise e


