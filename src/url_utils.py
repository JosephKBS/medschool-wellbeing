import re
from .config import IMAGE_EXTENSIONS


def is_valid_url(url):
    """Check if the URL has a valid format."""
    regex = re.compile(
        r'^(https?://)'
        r'([A-Za-z0-9.-]+)'
        r'(:\d+)?'
        r'(\/.*)?$'
    )
    return re.match(regex, url) is not None


def is_image_file(url):
    """Check if the URL points to an image file."""
    return url.lower().endswith(IMAGE_EXTENSIONS)


def extract_url_from_text(text):
    """Extract a clean URL from potentially messy CSV text (e.g. markdown links)."""
    url_match = re.search(r'https?://[^\s\]\)]+', str(text))
    return url_match.group(0) if url_match else text
