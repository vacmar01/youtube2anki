from tqdm import trange
import json
from pydantic import BaseModel, Field

class QuestionAnswer(BaseModel):
    """
    A question and answer pair that can be used to generate an anki card.
    """
    id: int = Field(..., description="monotonically increasing id")
    question: str
    answer: str

class QuestionAnswerSet(BaseModel):
    """
    A set of question and answer pairs that can be used to generate an anki deck.
    """

    questions: list[QuestionAnswer] = Field(..., description="list of questions and answers")
    
class AnkiCards:
    def __init__(self, youtube_client, llm_client):
        self.youtube_client = youtube_client
        self.llm_client = llm_client
    
    def get_questions_and_answers(self, chunk, n_questions):
        qas = self.llm_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Generate {n_questions} question and answers for this video transcript: \n{chunk}",
                }
            ],
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            response_model=QuestionAnswerSet,
            )
        
        return qas.questions
    
        
    def generate(self, text, n_questions, context_size=4096*4):
        results = []
        
        range = trange(0, len(text), context_size)
        n_questions_per_block = n_questions // len(range)
        for i in range:
            chunk = text[i:i+context_size]
            qas = self.get_questions_and_answers(chunk, n_questions_per_block)
            print(qas)
            results.extend(qas)
        return results