# %%
import os
import boto3
import boto3.s3
from dotenv import load_dotenv
from postgres_db_script import Metadata
import pandas as pd

# %%
load_dotenv()

# %%
goes_source_bucket = 'noaa-goes18'
team_source_bucket = os.environ.get('TARGET_BUCKET_NAME')


# %%
session = boto3.Session(
    region_name='us-east-1',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY_SECRET')
)


# %%
s3 = session.resource('s3')
from postgres_db_script import Metadata

# %%
src_bucket_goes = s3.Bucket(goes_source_bucket)
target_bucket = s3.Bucket(team_source_bucket)




import re
def get_aws_details_by_filename(filename):
    print("get_aws_details_by_filename")
    y = filename.split('_')
    # print(y)
    filename_pattern = r'(.*)-(.*)'
    regex_pattern = re.compile(filename_pattern)
    res_fn = regex_pattern.findall(y[1])
    res = str(res_fn[0][0])
    end = res[-1]
    if end.isnumeric():
        res = res[:-1]
            # print(res)
            # get timestamp
    time = y[3]
    year = time[1:5]
    day = time[5:8]
    hour = time[8:10]

    return year, day, hour

# %%
def get_all_geos_file_name_by_filter_new():
    files_available=[]
    metadata = Metadata()
    metadata.create_table_nexrad()
    station_id = "ABI-L1b-RadC"
    year = 2023
    print('********************** get_all_geos_file_name_by_filter_new****************')
    count = 0

    for object_summary in src_bucket_goes.objects.filter(Prefix=f'{station_id}/{year}/'):
        file_name = object_summary.key.split('/')[-1]
        files_available.append(file_name)
        year_new, day, hour = get_aws_details_by_filename(filename=file_name)
        metadata.insert_data_into_goes(station=station_id, year=year, day_of_year=day, hour=hour, filename=file_name)
        count+=1
        print(file_name)
        if count > 1000:
            break
    
    # metadata.db_conn_close()
    return files_available


# %%
# print(get_all_geos_file_name_by_filter_new('ABI-L1b-RadC', 2023))
# %%


def create_csv():
    metadata_instance = Metadata()
    conn = metadata_instance.conn_cursor_function() #, cursor

    goes_table_name = metadata_instance.get_goes_table_name()
    df1 = pd.read_sql_query("SELECT * FROM "+ goes_table_name, conn )

    nexrad_table_name = metadata_instance.get_nexrad_table_name()
    df2 = pd.read_sql_query("SELECT * FROM "+ nexrad_table_name, conn )

    filepath = './working_dir/data/'
    goes_csv_filename = 'GOES.csv'
    nexrad_csv_filename = 'NEXRAD.csv'

    df1.to_csv(filepath + goes_csv_filename ,index=False, sep=',')
    df2.to_csv(filepath + nexrad_csv_filename ,index=False, sep=',')
    
    metadata_instance.db_conn_close()