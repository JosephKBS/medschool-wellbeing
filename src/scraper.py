import time
import random

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from .config import REQUEST_TIMEOUT, DELAY_LOW, DELAY_HIGH
from .url_utils import is_valid_url, is_image_file


def smart_delay(low=DELAY_LOW, high=DELAY_HIGH):
    """Sleep for a random duration between low and high seconds."""
    time.sleep(random.uniform(low, high))


def extract_sub_websites(base_url):
    """Discover all same-domain subpage URLs from a base URL."""
    try:
        response = requests.get(base_url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        parsed_base = urlparse(base_url)
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(base_url, link['href'])
            parsed_url = urlparse(absolute_url)
            if parsed_base.netloc == parsed_url.netloc:
                if is_valid_url(absolute_url) and not is_image_file(absolute_url):
                    links.add(absolute_url)
        return sorted(links)
    except Exception as e:
        print(f"  Error fetching sub-websites from {base_url}: {e}")
        return []


def extract_page_text(url):
    """Extract main paragraph text from a single page.

    Removes nav, header, footer, sidebar, script, style elements.
    Looks for <main>, <article>, or div.content containers.
    Falls back to 'Main content not found' if no container found.
    """
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for element in soup(['nav', 'header', 'footer', 'sidebar', 'script', 'style']):
            element.decompose()
        main_content = (
            soup.find('main')
            or soup.find('article')
            or soup.find('div', class_='content')
        )
        if main_content:
            paragraphs = main_content.find_all('p')
            return ' '.join(p.get_text(strip=True) for p in paragraphs)
        else:
            return "Main content not found"
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None
