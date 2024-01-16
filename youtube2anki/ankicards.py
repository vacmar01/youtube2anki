from tqdm import trange
from .utils import sluggify
import json
import pandas as pd
from pydantic import BaseModel, model_validator

from typing import Any, List
import json


class Topics(BaseModel):
    """
    The three specific main topics of the transcript
    """
    topics: list[str]
    
    @model_validator(mode='before')
    @classmethod
    def validate_questions(cls, data):
        if str(data)[0] == "[": # if the first character is a bracket, assume it's a list of questions
            return {'topics': data}
        return data
    
class QuestionAnswer(BaseModel):
    """
    A pair of a question and an answer that test the user's understanding of the topic of the transcript
    """
    question: str
    answer: str
    
class QuestionAnswers(BaseModel):
    """
    A list of question and answer pairs that test the user's understanding of the topic of the transcript
    """
    questions: list[QuestionAnswer]
    
    @model_validator(mode='before')
    @classmethod
    def validate_questions(cls, data):
        if str(data)[0] == "[": # if the first character is a bracket, assume it's a list of questions
            return {'questions': data}
        return data
        

class AnkiCards:
    def __init__(self, youtube_client, llm_client, model_name="NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"):
        self.model_name = model_name
        self.youtube_client = youtube_client
        self.llm_client = llm_client
    
    def get_prompt(self, chunk, topics, n=3): 
        
        return f"""Generate {n} questions with correct answers to test the user's understanding of the following YouTube transcript. Focus on the main topics: {topics}. Aim for a mix of question types (e.g., multiple-choice, true/false, short answer) suitable for college students.

        Questions should vary in complexity, ranging from basic understanding to deeper analysis. Answers should be paraphrased from the transcript unless a direct quote is more appropriate. Keep questions and answers concise, ideally not exceeding 256 characters.

        Transcript: {chunk}"""
        
    def get_qas(self, prompt):
        return self.llm_client.chat.completions.create(
        model=self.model_name,
        response_model=QuestionAnswers,
        temperature=0.1,
        max_retries=3,
        messages=[
            {
                "role": "user", 
                "content": prompt
            },
        ],
    )
        
    def get_topics(self, chunk):
        topics = self.llm_client.chat.completions.create(
        model=self.model_name,
        response_model=Topics,
        max_retries=3,
        messages=[
            {
                "role": "user", 
                "content": f"extract the three main topics from the following video transcript: {chunk}"
            },
        ],
        temperature=0.2,
        )

        return topics.topics
        
        
    def generate(self, text, n_questions, context_size=4096*4):
        results = []
        
        range = trange(0, len(text), context_size)
        n_questions_per_block = n_questions // len(range)
        for i in range:
            chunk = text[i:i+context_size]
            prompt = self.get_prompt(chunk, n_questions_per_block, self.get_topics(chunk))
            qas = self.get_qas(prompt)
            results.append(qas)
        return list(set([json.loads(x.model_dump_json()) for x in qas.questions for qas in results]))