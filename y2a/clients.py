from isodate import parse_duration
import requests
from youtube_transcript_api import YouTubeTranscriptApi

class YoutubeClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://youtube.googleapis.com/youtube/v3"
    
    def get_data(self, id):
        r = requests.get(f"{self.base_url}/videos?part=snippet%2CcontentDetails&id={id}&key={self.api_key}")
        return r.json()
    
    def get_transcript(self, id):
        t = YouTubeTranscriptApi.get_transcript(id)
        return " ".join([x['text'] for x in t])
    
    def get_details(self, id):
        data = self.get_data(id)
        transcript = self.get_transcript(id)
        
        details = {
            'title': data['items'][0]['snippet']['title'],
            'channel': data['items'][0]['snippet']['channelTitle'],
            'transcript': transcript,
            'duration': parse_duration(data["items"][0]["contentDetails"]["duration"]).seconds,
        }
        
        return details
    