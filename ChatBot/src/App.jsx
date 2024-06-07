import { useState, useEffect, useRef } from "react";
import axios from "axios";
import pdfToText from "react-pdftotext";
import { IoMdSend } from "react-icons/io";
import ReactMarkdown from "react-markdown";
import { BsFillRecord2Fill } from "react-icons/bs";
import "./App.css";

const audioBlobToBase64 = (blob) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const arrayBuffer = reader.result;
      const base64Audio = btoa(
        new Uint8Array(arrayBuffer).reduce(
          (data, byte) => data + String.fromCharCode(byte),
          ""
        )
      );
      resolve(base64Audio);
    };
    reader.onerror = reject;
    reader.readAsArrayBuffer(blob);
  });
};

const AVAILABLE_MODELS = [
  'models/chat-bison-001', 'models/text-bison-001', 'models/embedding-gecko-001',
  'models/gemini-1.0-pro', 'models/gemini-1.0-pro-001', 'models/gemini-1.0-pro-latest',
  'models/gemini-1.0-pro-vision-latest', 'models/gemini-1.5-flash', 'models/gemini-1.5-flash-001',
  'models/gemini-1.5-flash-latest', 'models/gemini-1.5-pro', 'models/gemini-1.5-pro-001',
  'models/gemini-1.5-pro-latest', 'models/gemini-pro', 'models/gemini-pro-vision',
  'models/embedding-001', 'models/text-embedding-004', 'models/aqa'
];

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [transcription, setTranscription] = useState("");
  const [pdfText, setPdfText] = useState("");
  const [selectedModel, setSelectedModel] = useState(AVAILABLE_MODELS[0]);
  const msgRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    return () => {
      if (mediaRecorder) {
        mediaRecorder.stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [mediaRecorder]);

  useEffect(() => {
    msgRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages]);

  const apiKey = import.meta.env.VITE_GOOGLE_API_KEY;

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleModelChange = (e) => {
    setSelectedModel(e.target.value);
  };

  const handleSendMessage = async () => {
    if (input.trim() === "") return;

    const userMessage = { from: "user", text: input };
    setMessages([...messages, userMessage]);
    setInput("");

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: input, context: pdfText, model: selectedModel }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "An error occurred");
      }
      const botMessage = { from: "bot", text: data.response };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error(error);
      alert("An error occurred. Please try again.");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSendMessage();
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      recorder.start();
      console.log("Recording started");

      recorder.addEventListener("dataavailable", async (event) => {
        const audioBlob = event.data;
        const base64Audio = await audioBlobToBase64(audioBlob);

        try {
          const response = await axios.post(
            `https://speech.googleapis.com/v1/speech:recognize?key=${apiKey}`,
            {
              config: {
                encoding: "WEBM_OPUS",
                sampleRateHertz: 48000,
                languageCode: "en-US",
              },
              audio: {
                content: base64Audio,
              },
            }
          );

          if (response.data.results && response.data.results.length > 0) {
            setTranscription(
              response.data.results[0].alternatives[0].transcript
            );
            setInput(response.data.results[0].alternatives[0].transcript);
          } else {
            setTranscription("No transcription available");
          }
        } catch (error) {
          console.error(
            "Error with Google Speech-to-Text API:",
            error.response.data
          );
        }
      });

      setRecording(true);
      setMediaRecorder(recorder);
    } catch (error) {
      console.error("Error getting user media:", error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      console.log("Recording stopped");
      setRecording(false);
    }
  };

  const extractText = async (event) => {
    const file = event.target.files[0];
    try {
      const text = await pdfToText(file);
      setPdfText(text);
      alert("Text extracted successfully");
      // Clear the input field
      fileInputRef.current.value = "";
    } catch (error) {
      console.error("Failed to extract text from PDF", error);
    }
  };

  const clearPdfText = () => {
    setPdfText("");
    fileInputRef.current.value = "";
  };

  return (
    <div className="App">
      <div className="one_p">
        <div className="one_p chat_bot">
          <div className="title">
            <h2>AI Chat Bot</h2>
          </div>
          <div className="parent_chat">
            <div className="chat-window">
              {messages.map((msg, index) => (
                <div key={index} className={`message ${msg.from}`} ref={msgRef}>
                  <p className="txt">
                    <ReactMarkdown>{msg.text}</ReactMarkdown>
                  </p>
                </div>
              ))}
            </div>
            <div className="parent_prompt">
              <div className="prompt">
                <input
                  type="text"
                  className="msg"
                  value={input}
                  onChange={handleInputChange}
                  onKeyDown={handleKeyDown}
                />
                <button onClick={handleSendMessage} className="btn_send">
                  <IoMdSend />
                </button>
                <select value={selectedModel} onChange={handleModelChange} className="model_select">
                  {AVAILABLE_MODELS.map((model) => (
                    <option key={model} value={model}>
                      {model}
                    </option>
                  ))}
                </select>
              </div>
              <button
                onClick={recording ? stopRecording : startRecording}
                className="btn_record"
              >
                {recording ? "Stop" : "Start"}
                <BsFillRecord2Fill />
              </button>
            </div>
          </div>
        </div>
        <div className="vertical-line"></div>
        <div className="pdf-to-text">
          <div className="title">
            <h2>PDF Context Loader</h2>
          </div>
          <input
            type="file"
            className="self_center choose_btn"
            accept="application/pdf"
            onChange={extractText}
            ref={fileInputRef}
          />
          <div className="extracted-text">
            <h2 className="self_center">Extracted Text</h2>
            <pre>{pdfText}</pre>
          </div>
          <button onClick={clearPdfText} className="clear_btn">
            Clear
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
