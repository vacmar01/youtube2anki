from flask import Flask, request, render_template
from youtube2anki.clients import YoutubeClient, LLMClient
from youtube2anki.ankicards import AnkiCards
import os
import json
from math import ceil
from urllib.parse import urlparse, parse_qs

from dotenv import load_dotenv

load_dotenv()

youtube_api_key = os.getenv('YOUTUBE_API_KEY')
together_api_key = os.getenv('TOGETHER_API_KEY')
together_session_id = os.getenv('TOGETHER_SESSION_ID')

app = Flask(__name__)

youtube_client = YoutubeClient(youtube_api_key)
llm_client = LLMClient(together_api_key, together_session_id)

ak = AnkiCards(youtube_client, llm_client)

def youtube_id(url):
    parsed_url = urlparse(url)
    print(parsed_url)
    
    if not 'youtu' in parsed_url.netloc or parsed_url.netloc == '':
        print("Not a youtube url")
        raise ValueError("Not a youtube url")

    if 'youtu.be' in parsed_url.netloc:
        return parsed_url.path.split('/')[-1].split('?')[0]
    
    query_params = parse_qs(parsed_url.query)
    return query_params.get('v', [None])[0]

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/api/anki", methods=["GET"])
def generate():
    url = request.args.get('url')
    try:
        id = youtube_id(url)
        transcript = youtube_client.get_transcript(id)
        llm_context_size=4096*4
        n_questions = ceil(youtube_client.get_duration(id) / 60) // 5
        qas = ak.generate(transcript, n_questions=n_questions, context_size=llm_context_size)
        return render_template('qas.html', qas=qas)
    except Exception as e:
        return render_template('error.html', error=str(e))