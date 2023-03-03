#!/usr/bin/python3
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import os
import postgres_db_script as aws_fetch
import main as goes_filter
import nexrad_main as nexrad_filter
from datetime import datetime
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator
from great_expectations.data_context.types.base import (
    DataContextConfig,
    CheckpointConfig
)

base_path = "/opt/airflow/working_dir"
# data_dir = os.path.join(base_path, "News-Aggregator", "great_expectations", "data")
ge_root_dir = os.path.join(base_path, "great_expectations")
# report_dir = os.path.join(ge_root_dir, "uncommitted/data_docs/local_site/validations/nyt_raw_data_suite" )


dag = DAG(
    dag_id="sandbox",
    schedule="0 0 * * *",   # https://crontab.guru/
    catchup=False,
    start_date=datetime(2023, 3, 3),
    tags=["aws", "damg7245"],
)

with dag:

    # goes
    get_data_goes = PythonOperator(
        task_id='get_data_goes_from_aws',
        python_callable=goes_filter.get_all_geos_file_name_by_filter_new,
        dag=dag,
    )

    # nexrad
    get_data_nexrad = PythonOperator(
        task_id='get_data_nexrad_from_aws',
        python_callable=nexrad_filter.get_all_nexrad_file_name_by_filter_new,
        dag=dag,
    )

    # #csv both
    create_csv = PythonOperator(
        task_id='create_csv_from_db',
        python_callable=goes_filter.create_csv,
        dag=dag,
    )

    # ge_data_context_root_dir_with_checkpoint_name_pass = GreatExpectationsOperator(
    #     task_id="ge_data_context_root_dir_with_checkpoint_name_pass",
    #     data_context_root_dir=ge_root_dir,
    #     checkpoint_name="noaa_ck_version1",
    #     fail_task_on_validation_failure=False,
    #     dag=dag
    # )

    # Flow
    get_data_goes >> get_data_nexrad >> create_csv #>> ge_data_context_root_dir_with_checkpoint_name_pass
