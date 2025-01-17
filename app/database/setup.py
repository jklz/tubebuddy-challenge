# ensure imports work when calling directly as a part of app start script

from botocore.exceptions import ClientError
if __package__ is None or __package__ == '':
    from config import channel_metadata_table_name
    from client import dynamodb
else:
    from .config import channel_metadata_table_name
    from .client import dynamodb


def ensure_channel_table_exists() -> None:
    """
    Ensure that the dynamodb table for storing channel metadata has been created and has ttl setup.
    """

    # we need to use the client from the dynamodb resource
    dynamodb_client = dynamodb.meta.client

    try:
        # attempt to create the table for channel metadata

        dynamodb_client.create_table(
            TableName=channel_metadata_table_name,
            KeySchema=[
                {"AttributeName": "channel_id", "KeyType": "HASH"}, # Partition key
            ],
            AttributeDefinitions=[
                {"AttributeName": "channel_id", "AttributeType": "S"},
                {"AttributeName": "expiration_time", "AttributeType": "N"} # used for ttl, unix timestamp for when entry expires
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "ExpirationDateIndex",
                    "KeySchema": [
                        {"AttributeName": "expiration_time", "KeyType": "HASH"}
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    }
                }
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        )

        # wait for new table to be created
        table_exists_waiter = dynamodb_client.get_waiter('table_exists')
        table_exists_waiter.wait(TableName=channel_metadata_table_name)
        print('Table setup complete.')
    except dynamodb_client.exceptions.ResourceInUseException:
        # table already exists, nothing more we need to do
        pass

    # ensure ttl setup on table
    try:
        dynamodb_client.update_time_to_live (
            TableName=channel_metadata_table_name,
            TimeToLiveSpecification={
                "Enabled": True,
                "AttributeName": "expiration_time",
            }
        )
        print('TTL on table setup complete.')
    except (dynamodb_client.exceptions.ResourceInUseException, ClientError):
        # table already has ttl setup, nothing more we need to do
        pass

    except Exception as e:
        print('Error enabling TTL:', type(e))

# run to ensure that the table exists
ensure_channel_table_exists()
