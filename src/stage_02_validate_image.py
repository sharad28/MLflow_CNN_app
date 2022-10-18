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
from PIL import Image

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

    label1 = os.path.join(config["data"]['train'],config["data"]['label1']")
    label2 = os.path.join(config["data"]['train'],config["data"]['label2']")
    create_dir_label(local_dir,label1,label2)

def validate_data(source_dir,bad_img_dir):
    logging.info("Validation of images are started")
    for img in os.listdir(source_dir[0]):
        img_path = os.path.join(source_dir[0],img)
        bad_data_path = os.path.join(bad_img_dir[0],img)
        try:
            img1 = Image.open(img_path)
            img1.verify()

            if len(img1.getbands()) != 3 or imghdr.what(img_path) not in ['jpeg','png','jpg']:
                logging.error(f"length = {len(img1.getbands())} and format = {imghdr.what(img_path)}")
                shutil.move(img_path, bad_data_path)
                continue
            print(f"{img_path} is verified with format {imghdr.what(img_path)}")    
        except Exception as e:
            print(f"{img_path} is bad")            
            shutil.move(img_path,bad_data_path)
            raise e
    logging.info("Validation of images is completed")
    
def create_dir_label(local_dir,label1,label2):

    # label1 = os.path.join("train_data","class_1")
    # label2 = os.path.join("train_data","class_2")
    rest_img = []
    create_directories([label1,label2])
    for img in os.listdir(local_dir[0]):
        data_path = os.path.join(local_dir[0],img)
        if img.startswith("cat"):
            nw_path = os.path.join(label1,img)
            shutil.move(data_path,nw_path)
        elif img.startswith("dog"):
            nw_path = os.path.join(label2,img)
            shutil.move(data_path,nw_path)
        else:
            rest_img.append(img)
    logging.error(f"Following images are not moved to train data : {rest_img}")
    


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
        raise e