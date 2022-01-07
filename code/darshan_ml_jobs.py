import sys
import os
import pandas as pd
import glob
import numpy as np
from datetime import datetime 
import logging

log = logging.getLogger()

month=sys.argv[1]
day=sys.argv[2]

DARSHAN_DIR = os.getenv("DARSHAN_PARENT_DIR")
ML_KEYS='keras|training|solr_keras|candle_keras|tensorflow|interpolate|DeepBench|MonteCarlo_MachineLearning|sklearn|horovod|train|tf_cnn|stemdl|randomForest|pytorch|tensorflow|nt_train|cnn.pickle|convolutional.py|imagenet|sklearn|.tfrecord|ppi-cnn-gpu|ppi-3d-cnn|tensorboardX|train_tfrecord|cosmoFlow_cnn1|spDNN_data|DNN|Large_Batch_Training|epoch|regression|prediction|batch_size|federated-learning|sp1vfast3d_regression_ibm|sklearn|Pytorch|tf_cnn_benchmarks|tensorflow_synthetic_benchmark|STEMDL-Benchmark|FC-DenseNet|pytorch_synthetic_benchmark|network_FCDenseNet_custom|genomicPredictionRF|genomicPredictioniRF|iRF'

job_files = np.sort(glob.glob(f'{DARSHAN_DIR}/{month}/{day}/jobwise_darshan_restructure/*.csv'))
ai_jobs_df = pd.DataFrame()
for loop_cntr, j_f in enumerate(job_files):
    try:
        temp_job_df = pd.read_csv(j_f)
    except Exception as ex:
        message = f'An exception of type {type(ex).__name__} occurerd. Arguments: {ex.args} for {j_f}'
        print(message)
        continue
    ai_jobs_temp = temp_job_df[temp_job_df['filename'].str.contains(ML_KEYS)]
    if ai_jobs_temp.shape[0] > 0:
        #ai_jobs_temp['date']= datetime.strptime(f'{month[3:7]}-{month[0:3]}-{day}','%Y-%b-%d').date()
        job_date= datetime.strptime(f'{month[3:7]}-{month[0:3]}-{day}','%Y-%b-%d').date()
        job_id = job_id = int(j_f.split('/')[-1].split('.')[0])
        temp_jobs = pd.DataFrame({'job_id':job_id,'job_date':job_date},index=[0])
        ai_jobs_df = pd.concat([ai_jobs_df,temp_jobs],axis=0)     
save_path = f'{DARSHAN_DIR}/{month}/{day}/darshan_ml_keywords_jobs.csv'
ai_jobs_df.to_csv(save_path,index=False)
