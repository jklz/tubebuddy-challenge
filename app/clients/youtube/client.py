from app.clients.http.client import http_get
from app.clients.youtube.factory import parse_xml_feed_response


async def get_youtube_channel_feed(channel_id):
    """
    Get YouTube video feed for channel id
    """

    url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
    response = await http_get(url)
    if response.status_code != 200:
        # shouldn't happen for this endpoint
        return None
    return parse_xml_feed_response(response.text)

