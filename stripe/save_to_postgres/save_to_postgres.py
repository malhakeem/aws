import json
import boto3
import psycopg2
import logging
import traceback

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def make_connection():
    conn_str = "host=database-1.ctbvz04kso6g.us-east-2.rds.amazonaws.com dbname=postgres user=postgres password=postgrespw port=5432"
    conn = psycopg2.connect(conn_str)
    conn.autocommit = True
    return conn


def query_insert_data(event):
    data = event['data']
    data_object = data['object']

    id = data_object['id']
    object_field = data_object['object']
    created = data_object['created']
    livemode = data_object['livemode']
    paid = data_object['paid']
    amount = data_object['amount']
    currency = data_object['currency']
    refunded = data_object['refunded']
    source = json.dumps(data_object['source'])
    captured = data_object['captured']
    refunds = json.dumps(data_object['refunds'])
    balance_transaction = data_object['balance_transaction']
    failure_message = data_object['failure_message']
    failure_code = data_object['failure_code']
    amount_refunded = data_object['amount_refunded']
    customer = data_object['customer']
    invoice = data_object['invoice']
    description = data_object['description']
    dispute = data_object['dispute']
    metadata = json.dumps(data_object['metadata'])

    query = (id, object_field, created, livemode, paid, amount, currency, refunded, source, captured, refunds,
             balance_transaction, failure_message, failure_code,
             amount_refunded, customer, invoice, description, dispute, metadata)

    return query


def query_insert_stripe_source(event):
    created = event['created']
    livemode = event['livemode']
    id = event['id']
    type_val = event['type']
    object_val = event['object']

    query = (created, livemode, id, type_val, object_val)

    return query


def log_err(errmsg):
    logger.error(errmsg)
    return {"body": errmsg, "headers": {}, "statusCode": 400,
            "isBase64Encoded": "false"}


def lambda_handler(event, context):
    insert_data_query = "insert into public.stripe_data_object (id, object, created, livemode, paid, amount, currency, refunded, source, captured, refunds, \"balance_transaction\"," \
                        "failure_message, failure_code, amount_refunded, customer, invoice, description, dispute, metadata) values" \
                        "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    insert_stripe_source_query = "insert into public.stripe_source (created, livemode, id, \"type\", object, data_serial_id) values (%s, %s, %s, %s, %s, %s)"

    select_last_data_query = "select serial_id from public.stripe_data_object order by serial_id desc limit 1"
    last_data_serial_id = 0
    try:
        cnx = make_connection()
        cursor = cnx.cursor()

        # insert data table
        try:
            cursor.execute(insert_data_query, query_insert_data(event))
            cnx.commit()

        except:
            return log_err("ERROR: Cannot execute cursor.\n{}".format(traceback.format_exc()))

        # select last serial id from data_table
        try:
            cursor.execute(select_last_data_query)
            data = cursor.fetchall()

            for d in data:
                print(d)
                last_data_serial_id = d[0]

        except:
            return log_err("ERROR: Cannot execute cursor.\n{}".format(traceback.format_exc()))

        # insert stripe table
        try:
            values = query_insert_stripe_source(event)
            last_data_serial_id_tuple = (last_data_serial_id,)
            values = values + last_data_serial_id_tuple
            cursor.execute(insert_stripe_source_query, values)
            cnx.commit()
            cursor.close()
            cnx.close()

        except:
            return log_err("ERROR: Cannot execute cursor.\n{}".format(traceback.format_exc()))

    except:
        return 404

    return 200