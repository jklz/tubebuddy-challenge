import boto3

# dynamodb resource for connecting to dynamodb instance
# aws_access_key_id and aws_secret_access_key are required but don't impact dynamodb running locally
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url="http://tubebuddy-dynamodb:8000",
    region_name="us-west-2",
    aws_access_key_id='aaa',
    aws_secret_access_key='bbb',
)


