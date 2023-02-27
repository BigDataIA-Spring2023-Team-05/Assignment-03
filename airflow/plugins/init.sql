CREATE TABLE public.goes_data_table (station VARCHAR, year VARCHAR, day VARCHAR, hour VARCHAR, filename VARCHAR );

CREATE TABLE public.nexrad_data_table (year VARCHAR, month VARCHAR, date VARCHAR,  station VARCHAR, filename VARCHAR );

INSERT INTO public.goes_data_table (station, year, day, hour, filename) VALUES ('ABI-L1b-RadC', '2023', '053', '16', 'OR_ABI-L1b-RadC-M6C01_G16_s20230551601173_e20230551603546_c20230551603588.nc');
