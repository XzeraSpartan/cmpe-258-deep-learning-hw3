// src/api.js

const API_BASE_URL = "http://127.0.0.1:5000";

export async function transcribeAudio(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/transcribe`, {
    method: 'POST',
    body: formData,
  });

  const data = await response.json();
  return data.transcription;
}

export async function translateText() {
  const response = await fetch(`${API_BASE_URL}/translate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  const data = await response.json();
  return data.translation;
}

export async function summarizeText() {
  const response = await fetch(`${API_BASE_URL}/summarize`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  const data = await response.json();
  return data.summary;
}

export async function answerQuestion(question) {
  const response = await fetch(`${API_BASE_URL}/question-answer`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question }),
  });

  const data = await response.json();
  return data.answer;
}
