# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from model import transcribe_audio, translate_text, summarize_text, answer_question

app = Flask(__name__)
CORS(app)
# Global variable to store the transcribed text
transcribed_text = ""

@app.route('/transcribe', methods=['POST'])
def transcribe():
    global transcribed_text
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    file_path = './temp_audio.mp3'
    file.save(file_path)
    transcribed_text = transcribe_audio(file_path)
    return jsonify({'transcription': transcribed_text})

@app.route('/translate', methods=['POST'])
def translate():
    global transcribed_text
    if not transcribed_text:
        return jsonify({'error': 'No transcribed text available'}), 400
    translation = translate_text(transcribed_text)
    return jsonify({'translation': translation})

@app.route('/summarize', methods=['POST'])
def summarize():
    global transcribed_text
    if not transcribed_text:
        return jsonify({'error': 'No transcribed text available'}), 400
    summary = summarize_text(transcribed_text)
    return jsonify({'summary': summary})

@app.route('/question-answer', methods=['POST'])
def question_answer():
    global transcribed_text
    if not transcribed_text:
        return jsonify({'error': 'No transcribed text available'}), 400
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    answer = answer_question(question, transcribed_text)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
