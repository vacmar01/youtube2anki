from math import ceil
from tqdm import trange
from .utils import sluggify
import json
import pandas as pd

class AnkiCards:
    def __init__(self, youtube_client, llm_client):
        self.youtube_client = youtube_client
        self.llm_client = llm_client
    
    def get_prompt(self, chunk, n=3): 
        
        return f""" Generate {n} questions with correct and concise answers for the following youtube transcript to test your understanding of the content. 
        Provide the questions and answers as valid json in the following format:

        [{{"question": "question text", "answer": "answer text"}}, {{"question": "question text", "answer": "answer text"}} ... ]

        Transcript: {chunk}

        Answer only with the json string, nothing else. This is very important!
        """
        
    def generate(self, id, block_size=4096*4):
        transcript = self.youtube_client.get_transcript(id)
        results = []

        n_blocks = ceil(len(transcript) / block_size)
        n_questions = ceil(self.youtube_client.get_duration(id) / 60) // 5
        n_questions_per_block = n_questions // n_blocks
        
        for i in trange(0, len(transcript), block_size):
            chunk = transcript[i:i+block_size]
            prompt = self.get_prompt(chunk, n_questions_per_block)
            outp = self.llm_client.query(prompt)
            outp_text = outp["output"]["choices"][0]["text"]
            print(outp_text)
            try:
                result = json.loads(outp_text)
                result = json.loads(outp_text)
                results.extend(result)
                
            except:
                print("Error")
                print(outp_text)
        return results