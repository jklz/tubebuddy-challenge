import datetime
from fastapi import FastAPI, status, Response
from app.services.channel_metadata import get_metadata_for_channel, InvalidChannelLookupException


# create FastAPI app
app = FastAPI()

# add get route to return details for YouTube channel by channel_id
@app.get('/channels/{channel_id}', status_code=status.HTTP_200_OK)
async def get_channel(channel_id: str, response: Response):
    """
    Get channel metadata by channel_id
    """

    try:
        channel_metadata = await get_metadata_for_channel(channel_id)
        # return success response with channel metadata
        return {
            'status': 'success',
            'channel_id': channel_id,
            'title': channel_metadata['title'],
            'url': channel_metadata['url'],
            'recent_videos': channel_metadata['videos'],
        }
    except InvalidChannelLookupException:
        # requested channel_id was invalid,return 404 with error message
        response.status_code = status.HTTP_404_NOT_FOUND

        # return error response
        return {
            'status': 'error',
            'status_code': status.HTTP_404_NOT_FOUND,
            'error': {
                'message': 'The requested resource was not found.',
                'details': f'Unable to find metadata for channel {channel_id}.',
                'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
        }

