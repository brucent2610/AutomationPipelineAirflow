from airflow import DAG
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.contrib.operators.bigquery_check_operator import BigQueryCheckOperator

default_args = {
    'start_date': datetime(2023, 8, 25),
    'owner': 'Phong Nguyen',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

project_id = 'data-engineer-393307'
staging_dataset = 'ecommerce_newegg_staging'
production_dataset = 'ecommerce_newegg'
gs_bucket = 'data-engineer-393307-cloud-data-lake'

with DAG('newegg_cloud_data_lake_pipeline',
    schedule_interval=timedelta(days=1),
    default_args=default_args) as dag:

    start_pipeline = DummyOperator(task_id = 'start_pipeline')

    load_products = GoogleCloudStorageToBigQueryOperator(
        task_id = 'load_newegg_products',
        bucket = gs_bucket,
        source_objects = ['Products.csv'],
        destination_project_dataset_table = f'{project_id}:{staging_dataset}.products',
        write_disposition='WRITE_TRUNCATE',
        source_format="CSV",
        skip_leading_rows = 1,
        max_bad_records=100,
        autodetect=True,
        encoding="UTF-8",
        create_disposition="CREATE_IF_NEEDED",
    )

    check_us_cities_demo = BigQueryCheckOperator(
        task_id = 'check_newegg_products',
        use_legacy_sql=False,
        location="asia-northeast1",
        sql = f'SELECT count(*) FROM `{project_id}.{staging_dataset}.products`'
    )

    loaded_data_to_staging = DummyOperator(task_id = 'loaded_newegg_products_to_staging')

    end_pipeline = DummyOperator(task_id='end_pipeline')

    start_pipeline >> load_products >> check_us_cities_demo >> loaded_data_to_staging >> end_pipeline

    