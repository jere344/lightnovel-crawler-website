import unicodedata

def sanitize(text: str) -> str:
    """
    Remove all special characters from a string, replace accentuated characters with their
    non-accentuated counterparts, and remove all non-alphanumeric characters.
    """
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ").upper().strip()
    text = unicodedata.normalize("NFKD", text)
    return "".join([c for c in text if not unicodedata.combining(c)])