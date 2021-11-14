import apache_beam as beam
import argparse
from apache_beam.options.pipeline_options import PipelineOptions
from sys import argv
from apache_beam.dataframe import convert
import os

PROJECT_ID='red-function-330907'

def run(argv=None):
  parser = argparse.ArgumentParser()

  known_args, pipeline_args = parser.parse_known_args(argv)

  with beam.Pipeline(options=PipelineOptions()) as pipeline:
    extract_data = (
        pipeline 
        | 'Read CSV with beam.dataframe' >> beam.dataframe.io.read_csv('gs://de-week2-bucket/Data/*.csv') 
    )
    
    extract_data.fillna('',inplace=True)
    
    transform_data = (
        convert.to_pcollection(extract_data)
        | 'Convert to dictionaries' >> beam.Map(lambda x: dict(x._asdict()))
    )
    load_data = (
        transform_data
        | "Write data to BigQuery" >> beam.io.WriteToBigQuery(
           table= '{0}:flight1.all_flight'.format(PROJECT_ID),
           schema='SCHEMA_AUTODETECT',
           write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE)
    )
if __name__ == '__main__':
    run()
