import { useState, useEffect } from 'react';
import axios from 'axios';
import pdfToText from 'react-pdftotext';
import ReactMarkdown from 'react-markdown';
import './App.css';

const audioBlobToBase64 = (blob) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const arrayBuffer = reader.result;
      const base64Audio = btoa(
        new Uint8Array(arrayBuffer).reduce(
          (data, byte) => data + String.fromCharCode(byte),
          ''
        )
      );
      resolve(base64Audio);
    };
    reader.onerror = reject;
    reader.readAsArrayBuffer(blob);
  });
};

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [transcription, setTranscription] = useState('');
  const [pdfText, setPdfText] = useState('');

  useEffect(() => {
    return () => {
      if (mediaRecorder) {
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [mediaRecorder]);

  const apiKey = import.meta.env.VITE_GOOGLE_API_KEY;

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSendMessage = async () => {
    if (input.trim() === '') return;

    const userMessage = { from: 'user', text: input };
    setMessages([...messages, userMessage]);
    setInput('');

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input, context: pdfText }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'An error occurred');
      }
      const botMessage = { from: 'bot', text: data.response };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error(error);
      alert('An error occurred. Please try again.');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      recorder.start();
      console.log('Recording started');

      recorder.addEventListener('dataavailable', async (event) => {
        const audioBlob = event.data;
        const base64Audio = await audioBlobToBase64(audioBlob);

        try {
          const response = await axios.post(
            `https://speech.googleapis.com/v1/speech:recognize?key=${apiKey}`,
            {
              config: {
                encoding: 'WEBM_OPUS',
                sampleRateHertz: 48000,
                languageCode: 'en-US',
              },
              audio: {
                content: base64Audio,
              },
            }
          );

          if (response.data.results && response.data.results.length > 0) {
            setTranscription(response.data.results[0].alternatives[0].transcript);
            setInput(response.data.results[0].alternatives[0].transcript);
          } else {
            setTranscription('No transcription available');
          }
        } catch (error) {
          console.error('Error with Google Speech-to-Text API:', error.response.data);
        }
      });

      setRecording(true);
      setMediaRecorder(recorder);
    } catch (error) {
      console.error('Error getting user media:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      console.log('Recording stopped');
      setRecording(false);
    }
  };

  const extractText = async (event) => {
    const file = event.target.files[0];
    try {
      const text = await pdfToText(file);
      setPdfText(text);
      alert('Text extracted successfully');
    } catch (error) {
      console.error('Failed to extract text from PDF', error);
    }
  };

  return (
    <div className="App">
      <h1>Chatbot</h1>
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.from}`}>
            <ReactMarkdown>{msg.text}</ReactMarkdown>
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
      />
      <button onClick={handleSendMessage}>Send</button>

      <div className="speech-to-text">
        <h1>Speech to Text</h1>
        {!recording ? (
          <button onClick={startRecording}>Start Recording</button>
        ) : (
          <button onClick={stopRecording}>Stop Recording</button>
        )}
        <p>Transcription: {transcription}</p>
      </div>

      <div className="pdf-to-text">
        <h1>PDF to Text</h1>
        <input type="file" accept="application/pdf" onChange={extractText} />
        <div className="extracted-text">
          <h2>Extracted Text</h2>
          <pre>{pdfText}</pre>
        </div>
      </div>
    </div>
  );
}

export default App;
