
# AWS RDS Queries
available in queries.sql file

# AWS Stripe!

save to s3:
  - Update the S3 Bucket name and the path (line 13 & 14) where you would like to save the csv output in stripe/save_to_s3.py
  - create a new lambda function using Python 3.6 runtime and handler: save_to_s3.save_source_to_csv

save to postgres:
  - create tables using the scripts in stripe/save_to_postgres/create_stripe_data_object_table.sql and stripe/save_to_postgres/create_stripe_source_table.sql
  - update the postgres DB connection in stripe/save_to_postgres/save_to_postgres.py (line 12)
  - create new virtualenv in Python 3.6 locally and activate it
  - install requirements in requirements.txt
```sh
$ pip install -r requirements.txt
```
  - go to directory: venv/lib/python3.6/site-packages inside your project and copy stripe/save_to_postgres/save_to_postgres.py file in that directory
  - zip the files in site-packages directory and upload it to an S3 package
  - create a new lambda function and choose the zip file you uploaded as the code entry type, python 3.6 as runtime, and save_to_postgres.lambda_handler as the handler of the lambda function

Create the step function:
  - update the ARNs of the lambda functions in the stripe/save_to_postgres/step_function.json
  - create the state machine that runs the lambda functions in parallel 
  - create an API request and update the Stripe webhook accordingly
  - 
  
# Tests in mind (to be done)

  - test the structure of the json source file (making sure it has the hierarchy that is in the proposed json file)
  - test the existence of the of the S3 bucket and RDS postgres DB


