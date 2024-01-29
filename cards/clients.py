from y2a.clients import YoutubeClient
from y2a.ankicards import AnkiCards

from dotenv import load_dotenv
import os
import instructor
from openai import OpenAI

load_dotenv()

youtube_api_key = os.getenv('YOUTUBE_API_KEY')
together_api_key = os.getenv('TOGETHER_API_KEY')

youtube_client = YoutubeClient(youtube_api_key)

llm_client = instructor.patch(
    OpenAI(
        api_key=os.environ["TOGETHER_API_KEY"], 
        base_url='https://api.together.xyz/v1'
    ),
    mode=instructor.Mode.JSON_SCHEMA,
)

ankicards = AnkiCards(youtube_client, llm_client)