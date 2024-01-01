import re

def sluggify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", '', text)
    text = re.sub(r"\s+", '-', text)
    return text