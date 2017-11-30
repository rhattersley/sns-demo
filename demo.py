"""
A simple Flask application for receiving S3 events via an SNS topic.

It handles the initial subscription-confirmation step, and then
downloads all objects mentioned in any subsequent S3 event messages.

"""
from urllib import request
import json
import logging
import os.path

import boto3
import flask


app = flask.Flask(__name__)
app.logger.setLevel(logging.INFO)


S3 = boto3.client('s3')


@app.route('/target', methods=['POST'])
def target():
    body = flask.request.get_json(force=True)

    # In a production implementation we would verify the content
    # signature before continuing.

    message_type = body['Type']
    if message_type == 'SubscriptionConfirmation':
        # In a production implementation we would verify that we were
        # expecting to subscribe to the relevant SNS topic.

        # Confirm that we want to subscribe.
        request.urlopen(body['SubscribeURL'])

        app.logger.info('Confirmed subscription to {}'.format(
            body['TopicArn']))

    elif message_type == 'Notification':
        handle_s3_event_message(body['Message'])

    return 'OK'


def handle_s3_event_message(data):
    message = json.loads(data)
    for record in message['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        app.logger.info('Bucket: {}, key: {}'.format(bucket_name, object_key))
        bucket_region = S3.get_bucket_location(
            Bucket='mo-shub-sns-testing')['LocationConstraint']
        regional_s3 = boto3.client('s3', region_name=bucket_region)
        regional_s3.download_file(bucket_name, object_key,
                                  os.path.join('downloads', object_key))
