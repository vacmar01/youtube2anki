from isodate import parse_duration
import requests
from youtube_transcript_api import YouTubeTranscriptApi



class YoutubeClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://youtube.googleapis.com/youtube/v3"
    
    def get_details(self, id):
        r = requests.get(f"{self.base_url}/videos?part=snippet%2CcontentDetails&id={id}&key={self.api_key}")
        return r.json()

    def get_duration(self, id):
        o = self.get_details(id)
        #check if o has key items
        if "items" not in o:
            print(o)
            return
        duration = parse_duration(o["items"][0]["contentDetails"]["duration"])
        return duration.total_seconds()
    
    def get_transcript(self, id):
        t = YouTubeTranscriptApi.get_transcript(id)
        return " ".join([x['text'] for x in t])
    
    def get_videos_from_playlist(self, id):
        r = requests.get(f"{self.base_url}/playlistItems?part=snippet&playlistId={id}&key={self.api_key}")
        data = r.json()
        if "items" not in data:
            print(data)
            return
        print(data)
        return [item["id"] for item in data["items"]]

class LLMClient:
    def __init__(self, api_key, session_id):
        self.api_key = api_key
        self.session_id = session_id
        self.endpoint = 'https://api.together.xyz/inference'
    
    def query(self, prompt):
        res = requests.post(self.endpoint, json={
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "max_tokens": 1024,
            "prompt": f"[INST] {prompt} [/INST]",
            "request_type": "language-model-inference",
            "temperature": 0.3,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1,
            "stop": [
                "[/INST]",
                "</s>"
            ],
            "negative_prompt": "",
            "sessionKey": f"{self.session_id}"
        }, headers={
            "Authorization": f"Bearer {self.api_key}",
        })
        return res.json()
    