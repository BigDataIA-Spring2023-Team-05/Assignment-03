# %%
import os
import boto3
import boto3.s3
import botocore
from dotenv import load_dotenv
from postgres_db_script import Metadata

# %%
load_dotenv()

nexrad_source_bucket = 'noaa-nexrad-level2'
team_source_bucket = os.environ.get('TARGET_BUCKET_NAME')

# %%
session = boto3.Session(
    region_name='us-east-1',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY_SECRET')
)

# %%
s3 = session.resource('s3')

# %%
src_bucket_noaa = s3.Bucket(nexrad_source_bucket)
target_bucket = s3.Bucket(team_source_bucket)

#%%
def get_nexrad_aws_details_by_filename(filename):
    # write_nexrad_log(f"User requested  file: {filename}")
    print("get_nexrad_aws_details_by_filename")
    y = filename.split('_')[0]
    print(y)
    station = y[0:4]
    year = y[4:8]
    month = y[8:10]
    hour = y[10:12]

    return station ,year, month, hour

# %%
def get_all_nexrad_file_name_by_filter_new():
    files_available = []
    metadata = Metadata()
    metadata.create_table_nexrad()
    year = 2023
    print('********************** get_all_geos_file_name_by_filter_new****************')
    count = 0

    for object_summary in src_bucket_noaa.objects.filter(Prefix=f'{year}'): #/{month}/{day}/{station}
        file_name = object_summary.key.split('/')[-1]
        files_available.append(file_name)
        station ,year, month, hour = get_nexrad_aws_details_by_filename(filename=file_name)
        metadata.insert_data_into_nexrad(year=year, month=month, date=hour, station_id=station, filename=file_name)
        print(file_name)
        count+=1
        if count > 1000:
            break
    # metadata.db_conn_close()
    return files_available
