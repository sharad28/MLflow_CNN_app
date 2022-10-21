import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random
import tensorflow as tf
import mlflow


STAGE = "Train Stage" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs",'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path):
    
    ## read config files
    config = read_yaml(config_path)
    ## get ready the data
    parent_dir = config['data']['train']
    logging.info(f"read the data from parent dir")
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        parent_dir,
        validation_split=0.2,
        subset="training",
        seed=config['params']['seed'],
        image_size = config['params']['img_size'][:-1],
        batch_size = config['params']['batch_size']
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        parent_dir,
        validation_split=0.2,
        subset="validation",
        seed=config['params']['seed'],
        image_size = config['params']['img_size'][:-1],
        batch_size = config['params']['batch_size']
    )
    train_ds.prefetch(buffer_size= config['params']['buffer_size'])
    val_ds.prefetch(buffer_size = config['params']['buffer_size'])
    
    ## load the base model
    
    path_to_model = os.path.join(
        config["data"]["local_dir"][0],
        config["data"]["model_dir"],
        config['data']['init_model_file'])
    classifier = tf.keras.models.load_model(path_to_model)
    logging.info(f"load the based model")  
    #training
    logging.info(f"Training started")  
    classifier.fit(train_ds, epochs=config['params']['epochs'], validation_data=val_ds)
    train_model_file = os.path.join(
        config["data"]["local_dir"][0],
        config["data"]["model_dir"],
        config['data']['train_model_file'])

    classifier.save(train_model_file)
    logging.info(f"trained model is saved at :{train_model_file}")

    with mlflow.start_run() as runs:
        mlflow.log_params(params)
        mlflow.keras.log_model(classifier, "model")

    
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