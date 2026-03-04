import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data")

REQUEST_TIMEOUT = 30
DELAY_LOW = 0.3
DELAY_HIGH = 1.2
DELAY_BETWEEN_SCHOOLS_LOW = 1
DELAY_BETWEEN_SCHOOLS_HIGH = 2

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp')

STOP_WORDS = [
    'a', 'an', 'the', 'i', 'me', 'my', 'we', 'our', 'ours', 'you', 'your',
    'yours', 'he', 'him', 'his', 'she', 'her', 'hers', 'it', 'its', 'they', 'them',
    'their', 'theirs', 'what', 'which', 'who', 'whom', 'this', 'that', 'these',
    'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
    'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should',
    'in', 'on', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
    'and', 'but', 'or', 'because', 'as', 'until', 'while',
    'search', 'skip', 'menu', 'sub-navigation', 'news', 'close', 'contact us',
    'opens new tab', 'opens',
]
