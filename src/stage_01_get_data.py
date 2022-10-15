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

STAGE = "get_data" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path):
    ## read config files
    config = read_yaml(config_path)
    data_path = config['data']['data_source']
    local_dir = config['data']['local_dir']
    bad_img_dir = config['data']['bad_dir']
    create_directories(local_dir)
    create_directories(bad_img_dir)
    print(data_path,local_dir)
    moving_data(data_path,local_dir)
    pass


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    # args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        # main(config_path=parsed_args.config, params_path=parsed_args.params)
        main(config_path=parsed_args.config)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
