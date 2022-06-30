import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories

import random
import pandas as pd
from sklearn.model_selection import train_test_split

STAGE = "SPLIT DATA" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path, params_path):
    ## read config files
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    # Get artifacts dir..
    artifacts = config['artifacts']
    artifacts_dir = artifacts['ARTIFACTS_DIR']
    raw_local_dir = artifacts['RAW_LOCAL_DIR']
    raw_local_file = artifacts['RAW_LOCAL_FILE']
    split_data_dir = artifacts['SPLIT_DAT_DIR']

    test_size = params['base']['test_size']
    random_state = params['base']['random_state']

    raw_local_dir_path = os.path.join(artifacts_dir,raw_local_dir)

    raw_local_filepath = os.path.join(raw_local_dir_path,raw_local_file)
    
    logging.info(f'Data saved at path: {raw_local_filepath}')

    df = pd.read_csv(raw_local_filepath)
    
    df_train, df_test = train_test_split(df,test_size=test_size)
    logging.info(f'Splitting of data in training and test files. Split ratio has a test size of {test_size}')
    split_data_dir = artifacts['SPLIT_DAT_DIR']
    split_data_dir_path = os.path.join(artifacts_dir,split_data_dir)
    create_directories([split_data_dir_path])

    train_data_path = os.path.join(split_data_dir_path, artifacts['TRAIN'])
    test_data_path = os.path.join(split_data_dir_path, artifacts['TEST'])

    for data, data_path in (df_train, train_data_path), (df_test,test_data_path):
        data.to_csv(data_path,sep=',',index=False)
        logging.info(f'Data is saved at: {data_path}')

    pass


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config, params_path=parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e