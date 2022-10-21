import argparse
import os
import shutil
import tensorflow as tf
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

STAGE = "base_model" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path : dict) -> None:
    ## read config files
    config = read_yaml(config_path)
    input_shape = tuple(config['params']['img_size'])
    layers = [
        tf.keras.layers.Input(shape=input_shape),
        tf.keras.layers.Conv2D(filters=32, kernel_size=(3,3), activation='relu'),
        tf.keras.layers.MaxPool2D(pool_size=(2,2)),
        tf.keras.layers.Conv2D(filters=32,kernel_size=(3,3),activation="relu"),
        tf.keras.layers.MaxPool2D(pool_size=(2,2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(8,activation='relu'),
        tf.keras.layers.Dense(2,activation='softmax')
    ]
    classifier = tf.keras.Sequential(layers)
    classifier.summary(print_fn=logging.info)
    classifier.compile(
        optimizer =tf.keras.optimizers.Adam(learning_rate=config['params']['lr_rate']),
        loss = config['params']['loss'],
        metrics = config['params']['metrics']
    )
    
    path_to_model_dir = os.path.join(
        config["data"]["local_dir"][0],
        config["data"]["model_dir"]
    )
    create_directories([path_to_model_dir])
    path_to_model = os.path.join(
        path_to_model_dir,
        config['data']['init_model_file']
    )
    classifier.save(path_to_model)
    logging.info(f"model is saved at {path_to_model}")

    
    


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
