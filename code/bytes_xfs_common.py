import os
import glob
import pandas as pd
from datetime import datetime, timedelta
import glob
import numpy as np
import uuid # to generate a long key
import sys
import logging
import pdb

#pdb.set_trace()
log = logging.getLogger()

DARSHAN_DIR = os.getenv("DARSHAN_PARENT_DIR")
DARSHAN_SAVE_DIR = os.getenv("DARSHAN_ANALYSIS_DIR")
pd.options.mode.chained_assignment = None 
###
main_df = pd.DataFrame()
for i in range(0,1046,50):
    try:
        bb_persist_ = pd.read_csv(f'{DARSHAN_SAVE_DIR}/burst_buffer_persist_{i}.csv')
    except Exception as ex:
        print(i)
        continue
    main_df = pd.concat([main_df, bb_persist_],axis=0)

c_idx=int(sys.argv[1])

main_df = main_df.iloc[c_idx:c_idx+20,:].copy()
main_df = main_df.reset_index(drop=True)


main_df_persist = main_df#[main_df['persitence']>0]
bb_df_bytes = pd.DataFrame(columns=['total_read','total_write','xfs_read_val','xfs_write_val','common_read','common_write'])
for i in range(main_df_persist.shape[0]):
    print(i)
    job_id_ = int(main_df_persist['jobid'].iloc[i])
    date_ = datetime.strftime(datetime.strptime(main_df_persist['job_date'].iloc[i],"%Y-%m-%d"),'%Y-%b-%d')
    df_ = pd.read_csv(f'{DARSHAN_DIR}/{date_.split("-")[1]}{date_.split("-")[0]}/{int(date_.split("-")[2])}/jobwise_darshan_restructure/{job_id_}.csv')

    try:
        df_.loc[:,'MPIIO_POSIX_AGG_BYTES_WRITTEN'] = df_['MPIIO_BYTES_WRITTEN']
    except KeyError:
        df_.loc[:,'MPIIO_POSIX_AGG_BYTES_WRITTEN'] = np.nan
    try:
        df_.loc[:,'MPIIO_POSIX_AGG_BYTES_READ'] =  df_['MPIIO_BYTES_READ']
    except KeyError:
        df_.loc[:,'MPIIO_POSIX_AGG_BYTES_READ'] = np.nan
    #If MPIIO bytes READ or WRITTEN are NAN, replcae with POSIX READ and WRITE
    df_.loc[df_['MPIIO_POSIX_AGG_BYTES_WRITTEN'].isnull(),'MPIIO_POSIX_AGG_BYTES_WRITTEN'] = df_['POSIX_BYTES_WRITTEN'].round(2)
    df_.loc[df_['MPIIO_POSIX_AGG_BYTES_READ'].isnull(),'MPIIO_POSIX_AGG_BYTES_READ'] = df_['POSIX_BYTES_READ'].round(2)



    df_ = df_[df_['fstype'].isin(['gpfs','xfs'])]

    total_read = df_.loc[:,'MPIIO_POSIX_AGG_BYTES_READ'].fillna(0).sum()
    total_write = df_.loc[:,'MPIIO_POSIX_AGG_BYTES_WRITTEN'].fillna(0).sum()

    xfs_read_val = df_[df_['fstype']=='xfs'].loc[:,'MPIIO_POSIX_AGG_BYTES_READ'].fillna(0).sum()
    xfs_write_val = df_[df_['fstype']=='xfs'].loc[:,'MPIIO_POSIX_AGG_BYTES_WRITTEN'].fillna(0).sum()    

    gpfs_file_array = df_[df_['fstype']=='gpfs']['filename'].str.split("/").str[-1].values
    xfs_file_array = df_[df_['fstype']=='xfs']['filename'].str.split("/").str[-1].values

    common_files_set = np.intersect1d(xfs_file_array,gpfs_file_array)
    persist_file_list = list(xfs_file_array[np.isin(xfs_file_array,common_files_set)]) # to get multiple instance of one elem
    #pd.DataFrame({})
    common_files_set = set(common_files_set)
    uniq_val = str(uuid.uuid4()) # adding unique/random value so that search string never remains empty for str.contains function below
    search_set = common_files_set.copy()
    search_set.add(uniq_val)
    common_files_df =  (df_[df_['fstype']=='xfs'][(df_[df_['fstype']=='xfs']['filename'].str.contains('|'.join(list(search_set))))]).fillna(0)
    common_read = common_files_df.loc[:,'MPIIO_POSIX_AGG_BYTES_READ'].fillna(0).sum()
    common_write = common_files_df.loc[:,'MPIIO_POSIX_AGG_BYTES_WRITTEN'].fillna(0).sum()
        
    loop_df = (pd.DataFrame([{'jobid':str(job_id_), 'job_date':date_, 'total_read':total_read, 'total_write':total_write, 'xfs_read_val':xfs_read_val, 'xfs_write_val':xfs_write_val,
                 'common_read':common_read, 'common_write':common_write}],index=[0]))
    
    bb_df_bytes = pd.concat([bb_df_bytes,loop_df],axis=0)

bb_df_bytes.to_csv(f'{DARSHAN_SAVE_DIR}/bb_bytes_read_write/burst_buffer_bytes_read_write_{c_idx}.csv',index=False)
