import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]); // 👈 new state for Q&A history

  const askBackend = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setAnswer("");
    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();

      setAnswer(data.answer);
      // push query+answer into history
      setHistory((prev) => [...prev, { query, answer: data.answer }]);
      setQuery(""); // clear input
    } catch (err) {
      setAnswer("Error: Could not fetch response");
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: "700px", margin: "50px auto", fontFamily: "Arial" }}>
      <h2>📘 RAG Query System</h2>

      {/* --- Chat History --- */}
      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: "8px",
          padding: "10px",
          marginBottom: "20px",
          height: "400px",
          overflowY: "auto",
          background: "#fafafa",
        }}
      >
        {history.length === 0 && <p>No history yet. Ask something 👆</p>}

        {history.map((item, idx) => (
          <div key={idx} style={{ marginBottom: "15px" }}>
            <div
              style={{
                fontWeight: "bold",
                color: "#2c3e50",
                marginBottom: "5px",
              }}
            >
              Q: {item.query}
            </div>
            <div style={{ color: "#34495e", whiteSpace: "pre-line" }}>
              A: {item.answer}
            </div>
          </div>
        ))}
      </div>

      {/* --- Input --- */}
      <textarea
        rows="3"
        placeholder="Enter your question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: "100%", padding: "10px", fontSize: "16px" }}
      />
      <br />
      <button
        onClick={askBackend}
        disabled={loading}
        style={{
          marginTop: "10px",
          padding: "10px 20px",
          fontSize: "16px",
          cursor: "pointer",
        }}
      >
        {loading ? "Loading..." : "Ask"}
      </button>
    </div>
  );
}

export default App;
