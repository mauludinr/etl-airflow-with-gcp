
import apache_beam as beam
import argparse
from apache_beam.options.pipeline_options import PipelineOptions
from sys import argv
import os

PROJECT_ID='red-function-330907'

def run(argv=None):
  parser = argparse.ArgumentParser()

  known_args, pipeline_args = parser.parse_known_args(argv)

  with beam.Pipeline(options=PipelineOptions()) as pipeline:
    
    bq_table_schema = {
      "fields": [
        {
          "mode": "REQUIRED",
          "name": "searchTerms",
          "type": "STRING"
        },
        {
          "mode": "REQUIRED",
          "name": "querydate",
          "type": "STRING"
        },
        {
          "mode": "REQUIRED",
          "name": "search_count",
          "type": "INTEGER"
        },
      ]
    }
    
    output = (
	pipeline
        | "Read data from BigQuery" >> beam.io.ReadFromBigQuery(
                                  query='SELECT '
                                          'searchTerms,' 
                                          'FORMAT_TIMESTAMP("%Y-%m", queryTime) AS querydate,'
                                          'COUNT(searchTerms) AS search_count,' 
                                          'FROM `red-function-330907.flight1.all_flight`'
                                          'WHERE rank=1 GROUP BY searchTerms,querydate order by querydate ASC, search_count DESC'
                                  ,
                                  use_standard_sql=True)    
               

	| "Write data to BigQuery" >> beam.io.WriteToBigQuery(
           table= '{0}:flight1.most_searchedkeyword_month'.format(PROJECT_ID),
           schema= bq_table_schema,
           write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
	   create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
	   )
    )

if __name__ == '__main__':
    run()