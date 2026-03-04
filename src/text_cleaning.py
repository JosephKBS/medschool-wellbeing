import re
from .config import STOP_WORDS


def remove_stop_words(text, stop_words=None):
    """Remove stop words from text."""
    if stop_words is None:
        stop_words = STOP_WORDS
    words = text.split()
    filtered = [w for w in words if w.lower() not in stop_words]
    return ' '.join(filtered)


def clean_text(text):
    """Remove punctuation and stop words from text."""
    text = remove_stop_words(text)
    text = re.sub(r'[^\w\s]', '', text)
    return text


