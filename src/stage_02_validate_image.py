import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
from src.utils.common import moving_data
import random
from os import listdir
import numpy as np
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
import imghdr

STAGE = "validate_data" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path):
    ## read config files
    config = read_yaml(config_path)
    local_dir = config['data']['local_dir']
    bad_img_dir = config['data']['bad_dir']
    create_directories(bad_img_dir)
    validate_data(local_dir,bad_img_dir)
    pass

def validate_data(source_dir,bad_img_dir):
    logging.info("Validation of images are started")
    for img in os.listdir(source_dir[0]):
        img_path = os.path.join(source_dir[0],img)
        try:
            img1 = Image.open(img_path)
            img1.verify()

            if len(img1.getbands()) != 3 or imghdr.what(img_path) not in ['jpge','png']:
                bad_path = os.path.join(bad_img_dir[0],img)
                shutil.move(path_to_img, bad_data_path)
                continue
            print(f"{img_path}" is verified with format {imghdr.what(img_path)})    
        except Exception as e:
            print(f"{img_path} is bad")
            bad_data_path = os.path.join(bad_img_dir[0],img)
            shutil.move(img_path,bad_data_path)
    logging.info("Validation of images is completed")
    



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
