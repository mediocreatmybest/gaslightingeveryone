import argparse
import json

import pyarrow as pa
import pyarrow.parquet as pq
from pyarrow import json as pa_json
import pandas as pd


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some stuff.')
    parser.add_argument('--input-dir', type=str, required=False)
    parser.add_argument('--output-dir', type=str, required=False)
    args = parser.parse_args()

# https://arrow.apache.org/docs/python/parquet.html



# Start

# Load JSON from file
#with open('input.json') as f:
#    data = json.load(f)

# Convert JSON to table
table = pa_json.read_json('input.json')




# Write table to Parquet
pq.write_table(table, 'output.parquet')


# Open Parquet file
parquet_file = pq.ParquetFile('output.parquet')

parq_file = pd.read_parquet('output.parquet')

print(parq_file)

# Get Parquet schema
#parquet_schema = parquet_file.schema

#pq.read_table(parquet_file)

#print(parquet_schema)

# Print column names from schema
#for field in parquet_schema:
#    print(field.name, field)