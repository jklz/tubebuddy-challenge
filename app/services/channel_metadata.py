from app.clients.youtube.client import get_youtube_channel_feed
from app.database.channel_metadata import get_channel_metadata_item, put_channel_metadata_item
from app.clients.http.exceptions import HttpRequestException

class InvalidChannelLookupException(Exception):
    """
    Exception raised when an invalid channel lookup is encountered.
    """
    pass


async def get_metadata_for_channel(channel_id: str):
    """
    Get metadata for channel_id with utilizing a pass-threw cache on dynamodb
    """

    # attempt to get value from dynamodb
    dynamodb_data = get_channel_metadata_item(channel_id)

    if dynamodb_data is not None and 'metadata' in dynamodb_data:
        # received metadata from dynamodb
        return dynamodb_data['metadata']

    # no metadata for channel in dynamodb, need to pull YouTube feed for channel
    try:
        channel_feed_data = await get_youtube_channel_feed(channel_id)
        if channel_feed_data is None:
            # server didn't return as expected due to invalid channel_id
            raise InvalidChannelLookupException

    except HttpRequestException:
        # error in request from YouTube, passed channel_id is invalid
        raise InvalidChannelLookupException

    # store returned metadata for channel in dynamodb
    put_channel_metadata_item(channel_id, channel_feed_data)

    return channel_feed_data
