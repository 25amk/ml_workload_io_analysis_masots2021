import pandas as pd
from datetime import datetime, timedelta
import glob
import numpy as np
import logging
import os

log = logging.getLogger()
DARSHAN_PARENT_DIR = os.getenv("DARSHAN_PARENT_DIR")
path_1 = []
path_2 = []
path_3 = []
msng_schd_log_jobs_df = pd.read_csv('../processed_data/missing_jobs_in_schd_log.csv')
for i_ in range(msng_schd_log_jobs_df.shape[0]):
    
    job_date_ = datetime.strptime(msng_schd_log_jobs_df['job_date'].iloc[i_],'%Y-%m-%d')
    job_id_ = str(int(msng_schd_log_jobs_df['jobid'].iloc[i_]))
    job_date_str = datetime.strftime(job_date_,'%Y-%b-%d')
    job_year=job_date_str[0:4]
    job_month=job_date_str[5:8]
    job_date=str(int(job_date_str[9:]))
    t_ = pd.read_csv(f'{DARSHAN_PARENT_DIR}/{job_month}{job_year}/{job_date}/jobwise_darshan_restructure/{job_id_}.csv')
    print(i_)
    t1 = t_[t_['filename'].str.contains('gpfs')]
    t1 = pd.DataFrame(t1.iloc[0:1,:])
    path_1.append(t1['filename'].str.split("/").str[3].values[0])
    path_2.append(t1['filename'].str.split("/").str[4].values[0])
    path_3.append(t1['filename'].values[0])

msng_schd_log_jobs_df['path_1'] = path_1
msng_schd_log_jobs_df['path_2'] = path_2
msng_schd_log_jobs_df['path_3'] = path_3
msng_schd_log_jobs_df.to_csv('../processed_data/missing_jobs_in_schd_log_domain_path.csv',index=False)
