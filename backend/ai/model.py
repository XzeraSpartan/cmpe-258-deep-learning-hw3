# model.py

import torchaudio
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC, pipeline
from pydub import AudioSegment
import io

# Load the Wav2Vec2 processor and model for speech-to-text
asr_processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
asr_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")

# Load the translation pipeline
translation_pipeline = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")

# Load the summarization pipeline
summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

# Load the question answering pipeline
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

# Function to convert MP3 to a format torchaudio can process
def load_audio(file_path):
    audio = AudioSegment.from_file(file_path, format="mp3")
    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)
    waveform, sample_rate = torchaudio.load(buffer)
    return waveform, sample_rate

def transcribe_audio(file_path):
    waveform, sample_rate = load_audio(file_path)

    if sample_rate != 16000:
        waveform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(waveform)

    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0).unsqueeze(0)

    input_values = asr_processor(waveform.squeeze().numpy(), return_tensors="pt", sampling_rate=16000).input_values

    with torch.no_grad():
        logits = asr_model(input_values).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = asr_processor.decode(predicted_ids[0])

    return transcription

def translate_text(text):
    translated_text = translation_pipeline(text)
    return translated_text[0]['translation_text']

def summarize_text(text):
    summary = summarization_pipeline(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def answer_question(question, context):
    qa_input = {
        'question': question,
        'context': context
    }
    qa_output = qa_pipeline(qa_input)
    return qa_output['answer']
