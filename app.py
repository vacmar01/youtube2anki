# write a flask api with a single endpoint /anki that calls the AnkiCard generate method and returns the result

from flask import Flask, request, jsonify, render_template
from youtube2anki.clients import YoutubeClient, LLMClient
from youtube2anki.ankicards import AnkiCards
import os
import json

from dotenv import load_dotenv

load_dotenv()

youtube_api_key = os.getenv('youtube_api_key')
together_api_key = os.getenv('together_api_key')
together_session_id = os.getenv('together_session_key')

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
    return jsonify(ak.generate(id))
