import React, { useState } from "react";
import axios from "axios";

function App() {
  const [question, setQuestion] = useState("");
  const [hints, setHints] = useState({});
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    setError("");
    setHints({});

    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:5000/get-hints", { question });
      setHints(response.data);
    } catch (err) {
      setError(err.response?.data?.error || "An error occurred.");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6">
      <h1 className="text-2xl font-bold mb-4">AI Homework Helper</h1>
      <input
        type="text"
        className="w-full max-w-lg p-2 border rounded-lg"
        placeholder="Enter your question here..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button
        className="mt-3 px-4 py-2 bg-blue-500 text-white rounded-lg"
        onClick={handleSubmit}
      >
        Get Hints
      </button>

      {error && <p className="text-red-500 mt-3">{error}</p>}

      {hints.question && (
        <div className="mt-5 p-4 bg-white shadow rounded-lg w-full max-w-lg">
          <h2 className="font-semibold">Hints for: {hints.question}</h2>
          {Object.keys(hints)
            .filter((key) => key.startsWith("hint_"))
            .map((key, index) => (
              <p key={index} className="text-gray-700">{hints[key]}</p>
            ))}
          <h3 className="font-bold mt-4">Final Answer:</h3>
          <p className="text-gray-900">{hints.answer}</p>
        </div>
      )}
    </div>
  );
}

export default App;
