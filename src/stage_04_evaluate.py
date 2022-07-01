import argparse
import os
import shutil
from numpy.lib.npyio import save
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories, save_json
import random
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

STAGE = "EVAULATE" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )

def get_evaulation_metrics(df_actual, df_pred):
    rmse = np.sqrt(mean_squared_error(df_actual,df_pred))
    mae = mean_absolute_error(df_actual,df_pred)
    r2 = r2_score(df_actual,df_pred)

    scores = {
        'rmse':rmse,
        'mae':mae,
        'r2_score':r2
    }
    return scores
    pass

def main(config_path, params_path):
    ## read config files
    config = read_yaml(config_path)
    
    # Get from configs..
    artifacts = config['artifacts']
    artifacts_dir = artifacts['ARTIFACTS_DIR']
    split_data_dir = artifacts['SPLIT_DAT_DIR']
    model_dir = artifacts['MODEL_DIR']
    model_name = artifacts['MODEL_NAME']
    scores_file_path = config['scores']

    split_data_dir_path = os.path.join(artifacts_dir,split_data_dir)
    test_data_path = os.path.join(split_data_dir_path, artifacts['TEST'])
    
    model_dir_path = os.path.join(artifacts_dir,model_dir)
    create_directories([model_dir_path])
    model_file_path = os.path.join(model_dir_path,model_name)
    

    # Vars..
    target_col = 'quality'

    # LOGIC :
    df_test = pd.read_csv(test_data_path)
    
    df_y_test = df_test[target_col]
    df_X_test = df_test.drop([target_col],axis=1)

    lr = joblib.load(model_file_path)
    
    y_pred = lr.predict(df_X_test)
    
    scores = get_evaulation_metrics(df_y_test,y_pred)
    
    save_json(scores_file_path,scores)

    logging.info(f'Scores are evaluated and saved at saved at: {scores_file_path}')

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