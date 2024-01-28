from y2a.clients import YoutubeClient, LLMClient
from y2a.ankicards import AnkiCards

from dotenv import load_dotenv
import os

load_dotenv()

youtube_api_key = os.getenv('YOUTUBE_API_KEY')
together_api_key = os.getenv('TOGETHER_API_KEY')
together_session_id = os.getenv('TOGETHER_SESSION_ID')

youtube_client = YoutubeClient(youtube_api_key)
llm_client = LLMClient(together_api_key, together_session_id)

ankicards = AnkiCards(youtube_client, llm_client)