from urllib.parse import urlparse, parse_qs

def youtube_id(url):
    parsed_url = urlparse(url)
    
    if not 'youtu' in parsed_url.netloc or parsed_url.netloc == '':
        raise ValueError("Not a youtube url")

    if 'youtu.be' in parsed_url.netloc:
        return parsed_url.path.split('/')[-1].split('?')[0]
    
    query_params = parse_qs(parsed_url.query)
    return query_params.get('v', [None])[0]