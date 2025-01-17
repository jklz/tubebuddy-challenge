from xml.etree import ElementTree
from decimal import Decimal

def find_child_by_path(xml_element: ElementTree.Element, path: str, namespace_url: str = 'http://www.w3.org/2005/Atom'):
    """
    Lookup child element by path and namespace url
    """
    return xml_element.find('{' + namespace_url + '}' + path)

def find_yt_namespaced_child_by_path(xml_element: ElementTree.Element, path: str):
    """
    Lookup child element by path using YouTube namespace
    """
    return find_child_by_path(xml_element, path, 'http://www.youtube.com/xml/schemas/2015')

def find_media_namespaced_child_by_path(xml_element: ElementTree.Element, path: str):
    """
    Lookup child element by path using media namespace
    """
    return find_child_by_path(xml_element, path, 'http://search.yahoo.com/mrss/')

def parse_xml_feed_video_entry(video_entry: ElementTree.Element):
    """
    Parse YouTube video feed for channel video entry xml to an easily usable format
    """

    author_element = find_child_by_path(video_entry, 'author')
    media_group_element = find_media_namespaced_child_by_path(video_entry, 'group')
    thumbnail_element = find_media_namespaced_child_by_path(media_group_element, 'thumbnail')
    community_element = find_media_namespaced_child_by_path(media_group_element, 'community')
    star_rating_element = find_media_namespaced_child_by_path(community_element, 'starRating')
    statistics_element = find_media_namespaced_child_by_path(community_element, 'statistics')

    return {
        'video_id': find_yt_namespaced_child_by_path(video_entry, 'videoId').text,
        'title': find_child_by_path(video_entry, 'title').text,
        'link': find_child_by_path(video_entry, 'link').attrib['href'],
        'description': find_media_namespaced_child_by_path(media_group_element, 'description').text,
        'author': {
            'name': find_child_by_path(author_element, 'name').text,
            'url': find_child_by_path(author_element, 'uri').text,
        },
        'thumbnail': {
            'url': thumbnail_element.attrib['url'],
            'width': thumbnail_element.attrib['width'],
            'height': thumbnail_element.attrib['height'],
        },
        'statistics': {
            'views': int(statistics_element.attrib['views']),
            'star_rating': {
                'count': int(star_rating_element.attrib['count']),
                'average': Decimal(star_rating_element.attrib['average']),
                'min': int(star_rating_element.attrib['min']),
                'max': int(star_rating_element.attrib['max']),
            }
        },
        'published': find_child_by_path(video_entry, 'published').text,
        'updated': find_child_by_path(video_entry, 'updated').text,
    }

def parse_xml_feed_response(xml_body: str):
    """
    Parse YouTube video feed for channel xml to an easily usable format
    """

    xml = ElementTree.fromstring(xml_body)
    xml_video_entries = xml.findall('.//{http://www.w3.org/2005/Atom}entry')

    videos = []
    for xml_video_entry in xml_video_entries:
        videos.append(parse_xml_feed_video_entry(xml_video_entry))

    return {
        'title': find_child_by_path(xml, 'title').text,
        'url': find_child_by_path(xml, 'link[@rel="alternate"]').attrib['href'],
        'videos': videos
    }

