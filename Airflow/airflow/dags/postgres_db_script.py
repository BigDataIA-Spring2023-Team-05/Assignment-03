#%%
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import os
# import main as goes_filter
# import nexrad_main as nexrad_filter
import re

#%%
class Metadata():
    def __init__(self):

        #psycopg2
        BASE_URL = os.getenv("DB_URL", "postgresql://root:root@db:5432/noaa")
        # BASE_URL = "postgresql://root:root@db:5432/noaa"
        engine = create_engine(BASE_URL)
        self.conn = engine.connect()

        # db = scoped_session(sessionmaker(bind=engine))

        self.cursor = self.conn

        self.table_name_goes = 'goes_metadata'
        self.table_name_nexrad = 'nexrad_metadata'

        #for now
        # self.cursor = self.conn

    def drop_table_goes(self):
        self.cursor.execute(''' DROP TABLE IF EXISTS '''+ self.table_name_goes + ''';''')
        print("********** CREATED TABLE GOES ************")

    def drop_table_nexrad(self):
        self.cursor.execute(''' DROP TABLE IF EXISTS ''' + self.table_name_goes + ''';''')
        print("********** CREATED TABLE GOES ************")

    def create_table_goes(self):
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS '''+ self.table_name_goes + ''' (station VARCHAR, year VARCHAR, day VARCHAR ,hour VARCHAR, filename VARCHAR); ''')
        print("********** CREATED TABLE GOES ************")

    def create_table_nexrad(self):
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS '''+ self.table_name_nexrad + ''' (station VARCHAR, year VARCHAR, month VARCHAR, date VARCHAR, filename VARCHAR); ''')
        print("********** CREATED TABLE NEXRAD ************")

    def insert_data_into_goes(self, station, year, day_of_year, hour, filename):
        insert_str = 'INSERT INTO '+ self.table_name_goes+ ' (station, year, day, hour, filename) VALUES(' + '\''+ str(station) +'\'' +','+ '\''+ str(year)+'\'' +','+'\''+str(day_of_year)+'\'' +','+ '\''+str(hour)+'\'' +','+ '\''+str(filename)+'\''+');'
        self.cursor.execute(insert_str)
        print("insert "+insert_str)

    def insert_data_into_nexrad(self, year, month, date, station_id, filename):
        insert_str1 = 'INSERT INTO '+self.table_name_nexrad+' (station, year, month, date, filename) VALUES('+ '\''+str(year)+'\'' +','+ '\''+str(month)+'\'' +','+ '\''+str(date)+'\'' +','+ '\''+str(station_id)+'\'' +','+ '\''+str(filename)+'\''+');'
        self.cursor.execute(insert_str1)
        print("insert "+insert_str1)

    def print_and_validate_data_goes(self):
        self.cursor.execute("SELECT * FROM "+ self.table_name_goes)
        rows = self.cursor.fetchall()
        for row in rows:
            # Log().i(row)            
            print(row)
    
    def print_and_validate_data_nexrad(self):
        self.cursor.execute("SELECT * FROM "+ self.table_name_nexrad)
        rows = self.cursor.fetchall()
        for row in rows:
            # Log().i(row)            
            print(row)
    

    def db_conn_close(self):
        # self.conn.
        # Log().i('Data entered successfully.')
        print("Data is entered successfully.")
        self.conn.close()
        # Log().i("The Postgres connection is closed.")
        print("The Postgres connection is closed.")

    def conn_cursor_function(self):
        return self.conn
    #, self.cursor
    
    def get_goes_table_name(self):
        return self.table_name_goes
    
    def get_nexrad_table_name(self):
        return self.table_name_nexrad
    

#%%
# def initializing_db_with_data_from_aws_goes():
#     metadata_instance = Metadata()
#     # metadata_instance.drop_table_goes()
#     metadata_instance.create_table_goes()

#     ######### GOES ###########
#     try:
#         station_goes = "ABI-L1b-RadC"
#         year = 2023
#         goes_files_available_list = goes_filter.get_all_geos_file_name_by_filter_new(station_goes, year,)

#         print(len(goes_files_available_list))
#         print("executing goes_files_available_list")
#         for filename in goes_files_available_list:
#             if filename != "" and filename!=None:
#                 print(filename)
#                 year_new, day, hour = get_aws_details_by_filename(filename=filename)
#                 # metadata_instance.insert_data_into_goes(station=station_goes, year=year, day_of_year=day, hour=hour, filename=filename)
#     except TypeError:
#         print("Got NONE TYPE ***GOES*** ")
    # print_and_validate_data_goes

    # ######### CLOSE DB CONNECTIONS ###########
    # metadata_instance.db_conn_close()

#%%
# def initializing_db_with_data_from_aws_nexrad():
    
#     metadata_instance = Metadata()
#     # metadata_instance.drop_table_nexrad()
#     metadata_instance.create_table_goes()

#     ######### NEXRAD ###########
#     try:
#         year = '2023'
#         nexrad_files_available_list = nexrad_filter.get_all_nexrad_file_name_by_filter_new(year)
#         for filename in nexrad_files_available_list:
#             if filename != "" and filename!=None:
#                 print(filename)
#                 station_nexrad, year_nex, month, hour = get_nexrad_aws_details_by_filename(filename=filename)  
#                 metadata_instance.insert_data_into_nexrad(year=year, month=month, date=hour,  station_id=station_nexrad, filename=filename)
#     except TypeError:
#         print("Got NONE TYPE ***GOES*** ")

# #%%
# def create_csv():
#     metadata_instance = Metadata()
#     conn = metadata_instance.conn_cursor_function() #, cursor
#     goes_table_name = metadata_instance.get_goes_table_name()
#     df1 = pd.read_sql_query("SELECT * FROM "+ goes_table_name, conn )
#     nexrad_table_name = metadata_instance.get_nexrad_table_name()
#     df2 = pd.read_sql_query("SELECT * FROM "+ nexrad_table_name, conn )
#     filepath = './working_dir/data/'
#     goes_csv_filename = 'GOES.csv'
#     nexrad_csv_filename = 'NEXRAD.csv'
#     df1.to_csv(filepath + goes_csv_filename ,index=False)
#     df2.to_csv(filepath + nexrad_csv_filename ,index=False)
#     metadata_instance.db_conn_close()

# #%%
# import re
# def get_aws_details_by_filename(filename):
#     print("get_aws_details_by_filename")
#     y = filename.split('_')
#     # print(y)
#     filename_pattern = r'(.*)-(.*)'
#     regex_pattern = re.compile(filename_pattern)
#     res_fn = regex_pattern.findall(y[1])
#     res = str(res_fn[0][0])
#     end = res[-1]
#     if end.isnumeric():
#         res = res[:-1]
#             # print(res)
#             # get timestamp
#     time = y[3]
#     year = time[1:5]
#     day = time[5:8]
#     hour = time[8:10]

#     return year, day, hour

# #%%
# def get_nexrad_aws_details_by_filename(filename):
#     # write_nexrad_log(f"User requested  file: {filename}")
#     print("get_nexrad_aws_details_by_filename")
#     y = filename.split('_')[0]
#     print(y)
#     station = y[0:4]
#     year = y[4:8]
#     month = y[8:10]
#     hour = y[10:12]

#     return station ,year, month, hour


#%%S
# initializing_db_with_data_from_aws()
# create_csv()

#%%
# filename = "OR_ABI-L1b-RadC-M6C14_G18_s20230022256173_e20230022258546_c20230022259026.nc"
# year, day, hour = get_aws_details_by_filename(filename)
# print(year, day, hour)
# # %%
# filename = "KJGX19700101_000000_V06"
# station ,year, month, hour = get_nexrad_aws_details_by_filename(filename)
# print(station ,year, month, hour)