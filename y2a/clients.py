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
        return res.json()["output"]["choices"][0]["text"]
    