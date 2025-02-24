import React, { useState } from "react";
import axios from "axios";
import { MathJax, MathJaxContext } from "better-react-mathjax";
import { ClipLoader } from "react-spinners"; 

function App() {
  const [question, setQuestion] = useState("");
  const [hints, setHints] = useState({});
  const [error, setError] = useState("");
  const [visibleHints, setVisibleHints] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setError("");
    setHints({});
    setVisibleHints(0);
    setShowAnswer(false);
    setLoading(true);

    if (!question.trim()) {
      setError("Please enter a question.");
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post("http://localhost:5000/get-hints", { question });
      setHints(response.data);
    } catch (err) {
      setError(err.response?.data?.error || "Please enter a valid question.");
    }

    setLoading(false);
  };

  return (
    <MathJaxContext>
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6 font-noto">
        <h1 className="text-2xl font-bold mb-4">HintWise</h1>
        <textarea
          className="w-full max-w-lg p-4 border rounded-lg overflow-auto"
          rows={1}
          placeholder="Enter your question here..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button
          className="mt-3 px-4 py-2 bg-blue-500 text-white rounded-lg"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? "Loading..." : "Get Hints"}
        </button>

        {error && <p className="text-red-500 mt-3">{error}</p>}

        {loading && (
          <div className="mt-4 text-center">
            <ClipLoader color="#4B8BF4" loading={loading} size={50} />
            <p className="text-gray-600 mt-3">Generating hints...</p>
          </div>
        )}

        {hints.question && !loading && (
          <div className="mt-5 p-4 bg-white shadow rounded-lg w-full max-w-lg">
            <h2 className="font-semibold">Your Question: {hints.question}</h2>

            {Object.keys(hints)
              .filter((key) => key.startsWith("hint_"))
              .map((key, index) => (
                <div key={index} className="mt-2">
                  {index < visibleHints ? (
                    <p className="text-gray-700">
                      <MathJax>{hints[key]}</MathJax>
                    </p>
                  ) : (
                    <button
                      className="text-blue-500 underline"
                      onClick={() => setVisibleHints(index + 1)}
                    >
                      Show Hint {index + 1}
                    </button>
                  )}
                </div>
              ))}

            {!showAnswer ? (
              <button
                className="mt-3 px-4 py-2 bg-green-500 text-white rounded-lg"
                onClick={() => setShowAnswer(true)}
              >
                Show Answer
              </button>
            ) : (
              <div className="mt-3">
                <h3 className="font-bold">Final Answer:</h3>
                <p className="text-gray-900">
                  <MathJax>{hints.answer}</MathJax>
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </MathJaxContext>
  );
}

export default App;
