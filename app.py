from flask import Flask, request, jsonify, render_template
from youtube2anki.clients import YoutubeClient, LLMClient
from youtube2anki.ankicards import AnkiCards
import os
import json
from math import ceil

from dotenv import load_dotenv

load_dotenv()

youtube_api_key = os.getenv('YOUTUBE_API_KEY')
together_api_key = os.getenv('TOGETHER_API_KEY')
together_session_id = os.getenv('TOGETHER_SESSION_ID')

app = Flask(__name__)

youtube_client = YoutubeClient(youtube_api_key)
llm_client = LLMClient(together_api_key, together_session_id)

ak = AnkiCards(youtube_client, llm_client)

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/api/anki", methods=["GET"])
def generate():
    id = request.args.get('id')
    try:
        transcript = youtube_client.get_transcript(id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    llm_context_size=4096*4
    n_questions = ceil(youtube_client.get_duration(id) / 60) // 5
    
    try: 
        qas = ak.generate(transcript, n_questions=n_questions, context_size=llm_context_size)
        return jsonify(qas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
