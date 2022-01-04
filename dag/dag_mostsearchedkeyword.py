import os
from airflow import DAG
from airflow.providers.apache.beam.operators.beam import BeamRunPythonPipelineOperator
from airflow.providers.google.cloud.operators.dataflow import DataflowConfiguration
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow import configuration
from airflow.models import Variable
from datetime import datetime


args = {
 
    'owner': 'mauludinr98',
    'start_date': datetime(2021,10,30),
    'retries' : 1,
}

PROJECT_ID = 'red-function-330907'
PY_FILE1 = ('gs://de-week2-bucket/project_flight/dataflow/keysearchmonth_bq.py')
PY_FILE2 = ('gs://de-week2-bucket/project_flight/dataflow/keysearchyear_bq.py')
pipeline_options = {'tempLocation': "gs://de-week2-bucket/batch/stag" ,
                    'stagingLocation': "gs://de-week2-bucket/batch/temp",
                        }


dag = DAG(dag_id = 'dag_mostsearchedkeyword', default_args=args,catchup=False, schedule_interval='@daily')
 
with dag:
    searchkeyword_month = BeamRunPythonPipelineOperator(
        task_id='keyword_search_month_bigquery',
        runner='DataflowRunner',
        gcp_conn_id='google_cloud_default',
        py_file=PY_FILE1,
        py_requirements=['apache-beam[gcp]==2.34.0'],
        py_system_site_packages=True,
        py_interpreter='python3',
        pipeline_options=pipeline_options,
        dataflow_config=DataflowConfiguration(
            job_name="keywordsearch_month_{{ ds_nodash }}",
            project_id=PROJECT_ID,
            location="asia-southeast1",
            wait_until_finished=True
        )
    )
    searchkeyword_year = BeamRunPythonPipelineOperator(
        task_id='keyword_search_year_bigquery',
        runner='DataflowRunner',
        gcp_conn_id='google_cloud_default',
        py_file=PY_FILE2,
        py_requirements=['apache-beam[gcp]==2.34.0'],
        py_system_site_packages=True,
        py_interpreter='python3',
        pipeline_options=pipeline_options,
        dataflow_config=DataflowConfiguration(
            job_name="keywordsearch_year_{{ ds_nodash }}",
            project_id=PROJECT_ID,
            location="asia-southeast1",
            wait_until_finished=True
        )
    )

    searchkeyword_month >> searchkeyword_year


