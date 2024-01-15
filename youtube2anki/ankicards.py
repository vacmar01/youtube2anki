from tqdm import trange
from .utils import sluggify
import json
import pandas as pd

class AnkiCards:
    def __init__(self, youtube_client, llm_client):
        self.youtube_client = youtube_client
        self.llm_client = llm_client
    
    def get_prompt(self, chunk, n=3): 
        
        return f""" Generate {n} questions with correct answers for the following youtube transcript to test the user's understanding of the video's content.
    
        Questions should vary in complexity, ranging from basic understanding to deeper analysis. Answers should be paraphrased from the transcript unless a direct quote is more appropriate. Keep questions and answers concise, ideally not exceeding 256 characters each.
         
        Provide the questions and answers as valid json in the following format:

        [{{"question": "question text", "answer": "answer text"}}, {{"question": "question text", "answer": "answer text"}} ... ]

        Transcript: {chunk}

        Answer only with the json string, nothing else. This is very important!
        """
        
    def generate(self, text, n_questions, context_size=4096*4):
        results = []
        
        range = trange(0, len(text), context_size)
        n_questions_per_block = n_questions // len(range)
        for i in range:
            chunk = text[i:i+context_size]
            prompt = self.get_prompt(chunk, n_questions_per_block)
            outp_text = self.llm_client.query(prompt)
            print(outp_text)
            try:
                result = json.loads(outp_text)
                results.extend(result)
            except:
                print("Error")
                print(outp_text)
        return results