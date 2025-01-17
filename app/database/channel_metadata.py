import time
from app.database.client import dynamodb
from app.database.config import channel_metadata_table_name, channel_metadata_ttl_sec

# dynamodb table connection
channel_metadata_table_resource = dynamodb.Table(channel_metadata_table_name)


def put_channel_metadata_item(channel_id: str, metadata) -> None:
    """
    Store channel metadata in dynamodb table with TTL of 24 hours
    """

    # Calculate the expiration time in Unix timestamp
    expiration_time = int(time.time()) + channel_metadata_ttl_sec

    # put item in table
    channel_metadata_table_resource.put_item(
        Item={
            'channel_id': channel_id,
            'metadata': metadata,
            'expiration_time': expiration_time,
        }
    )

def get_channel_metadata_item(channel_id: str):
    """
    Get channel metadata from dynamodb table if exists
    """

    # request item from table by key(channel_id)
    response = channel_metadata_table_resource.get_item(Key={'channel_id': channel_id})

    if 'Item' in response:
        # item was included in response, return response data
        return response['Item']

    # dynamodb did not include data for requested channel_id
    return None

