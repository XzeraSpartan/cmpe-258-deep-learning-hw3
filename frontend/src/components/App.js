// src/components/App.js

import React, { useState } from 'react';
import { transcribeAudio, translateText, summarizeText, answerQuestion } from '../api';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [transcription, setTranscription] = useState('');
  const [translation, setTranslation] = useState('');
  const [summary, setSummary] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleTranscribe = async () => {
    if (file) {
      const transcription = await transcribeAudio(file);
      setTranscription(transcription);
      setTranslation('');
      setSummary('');
      setAnswer('');
    }
  };

  const handleTranslate = async () => {
    if (transcription) {
      const translation = await translateText();
      setTranslation(translation);
    }
  };

  const handleSummarize = async () => {
    if (transcription) {
      const summary = await summarizeText();
      setSummary(summary);
    }
  };

  const handleQuestionAnswer = async () => {
    if (transcription && question) {
      const answer = await answerQuestion(question);
      setAnswer(answer);
    }
  };

  return (
    <div className="App">
      <h1>Audio Processing App</h1>
      <div className="input-container">
        <label className="input" htmlFor="file-input">Choose file</label>
        <input 
          type="file" 
          accept="audio/*" 
          id="file-input" 
          className="input-file" 
          onChange={handleFileChange} 
        />
      </div>
      <button onClick={handleTranscribe}>Transcribe</button>
      <button onClick={handleTranslate}>Translate</button>
      <button onClick={handleSummarize}>Summarize</button>
      <div>
        <input
          type="text"
          placeholder="Enter your question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="input"
        />
        <button onClick={handleQuestionAnswer}>Answer Question</button>
      </div>
      <div className="output">
        {transcription && <div><h2>Transcription:</h2><p>{transcription}</p></div>}
        {translation && <div><h2>Translation:</h2><p>{translation}</p></div>}
        {summary && <div><h2>Summary:</h2><p>{summary}</p></div>}
        {answer && <div><h2>Answer:</h2><p>{answer}</p></div>}
      </div>
    </div>
  );
}

export default App;
