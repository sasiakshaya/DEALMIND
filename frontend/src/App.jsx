import { useEffect, useState } from "react";
import "./index.css";

const API = import.meta.env.VITE_API_URL || "";
const DEAL_ID = "acme-001";

function formatDate(value) {
  if (!value) return "";
  const [year, month, day] = value.split("-");
  return new Date(Number(year), Number(month) - 1, Number(day)).toLocaleDateString(
    "en-US",
    {
      month: "short",
      day: "2-digit",
      year: "numeric",
    }
  );
}

function App() {
  const [deal, setDeal] = useState(null);
  const [newInteraction, setNewInteraction] = useState("");
  const [question, setQuestion] = useState("");
  const [memories, setMemories] = useState([]);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("overview");
  const [message, setMessage] = useState("");

  async function loadDeal() {
    try {
      const response = await fetch(`${API}/api/deals/${DEAL_ID}`);
      const raw = await response.text();

      if (!response.ok) {
        throw new Error(`Backend error ${response.status}`);
      }

      const data = JSON.parse(raw);
      setDeal(data);
    } catch {
      setMessage("Backend is not reachable. Make sure FastAPI is running.");
    }
  }

  useEffect(() => {
    loadDeal();
  }, []);

  async function addInteraction() {
    if (!newInteraction.trim()) return;

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(
        `${API}/api/deals/${DEAL_ID}/interactions`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: newInteraction.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed");
      }

      setNewInteraction("");
      setMessage("Saved to DealMind + Hindsight memory.");
      await loadDeal();
    } catch (error) {
      setMessage(error.message || "Could not save interaction.");
    } finally {
      setLoading(false);
    }
  }

  async function askDeal() {
    if (!question.trim()) return;

    setLoading(true);
    setMemories([]);
    setMessage("");

    try {
      const response = await fetch(`${API}/api/deals/recall`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          deal_id: DEAL_ID,
          question: question.trim(),
        }),
      });

      const raw = await response.text();

      if (!response.ok) {
        throw new Error(`Backend error ${response.status}`);
      }

      const data = JSON.parse(raw);

      setMemories(data.memories || []);
    } catch (error) {
      setMessage(error.message || "Could not retrieve Hindsight memory.");
    } finally {
      setLoading(false);
    }
  }

  async function prepareMeeting() {
    setLoading(true);
    setAnswer("");
    setActiveTab("intelligence");
    setMessage("");

    try {
      const response = await fetch(`${API}/api/deals/reflect`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          deal_id: DEAL_ID,
          question:
            "Prepare me for my next meeting with ACME Corp. Tell me what I should know, the main risks, and what actions I should take.",
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error("Preparation failed");
      }

      let cleaned = data.answer || "No preparation was generated.";

      cleaned = cleaned.replace(
        /(?:scheduled|associated with|between|from)?\s*October 5, 2026(?:\s*,?\s*(?:and|to|-)\s*October 11, 2026)?/gi,
        "next week"
      );

      cleaned = cleaned.replace(/\\#/g, "#");

      setAnswer(cleaned);
    } catch (error) {
      setMessage(error.message || "Could not generate meeting preparation.");
    } finally {
      setLoading(false);
    }
  }

  if (!deal) {
    return (
      <div
        style={{
          minHeight: "100vh",
          display: "grid",
          placeItems: "center",
          fontFamily: "system-ui",
        }}
      >
        <div>
          <h2>Loading DealMind...</h2>
          <p>{message}</p>
        </div>
      </div>
    );
  }

  const interactions = [...deal.interactions].reverse();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">D</div>
          <div>
            <div className="brand-name">DealMind</div>
            <div className="brand-tag">AI Deal Intelligence</div>
          </div>
        </div>

        <nav>
          <button
            className={activeTab === "overview" ? "nav-item active" : "nav-item"}
            onClick={() => setActiveTab("overview")}
          >
            <span>◉</span> Overview
          </button>

          <button
            className={activeTab === "timeline" ? "nav-item active" : "nav-item"}
            onClick={() => setActiveTab("timeline")}
          >
            <span>◷</span> Deal Timeline
          </button>

          <button
            className={activeTab === "memory" ? "nav-item active" : "nav-item"}
            onClick={() => setActiveTab("memory")}
          >
            <span>✦</span> Hindsight Memory
          </button>

          <button
            className={activeTab === "intelligence" ? "nav-item active" : "nav-item"}
            onClick={() => setActiveTab("intelligence")}
          >
            <span>✧</span> AI Intelligence
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="memory-status">
            <div className="status-dot"></div>
            <div>
              <strong>Hindsight Connected</strong>
              <span>Persistent memory active</span>
            </div>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">DEAL INTELLIGENCE</p>
            <h1>{deal.company}</h1>
            <p className="subtext">
              {deal.product} <span>•</span> {deal.deal_id}
            </p>
          </div>

          <button className="prepare-btn" onClick={prepareMeeting}>
            ✦ Prepare Me for Meeting
          </button>
        </header>

        {message && <div className="notice">{message}</div>}

        {activeTab === "overview" && (
          <>
            <section className="metrics-grid">
              <div className="metric-card">
                <span>Deal Stage</span>
                <strong>{deal.stage}</strong>
                <small>Revised pricing requested</small>
              </div>

              <div className="metric-card">
                <span>Memory Events</span>
                <strong>{deal.interactions.length}</strong>
                <small>Persisted deal interactions</small>
              </div>

              <div className="metric-card risk">
                <span>Deal Risk</span>
                <strong>Medium</strong>
                <small>Pricing + competition</small>
              </div>

              <div className="metric-card">
                <span>Decision Maker</span>
                <strong>CTO</strong>
                <small>Technical approval required</small>
              </div>
            </section>

            <section className="content-grid">
              <div className="panel">
                <div className="panel-header">
                  <div>
                    <p className="panel-label">RECENT CONTEXT</p>
                    <h2>What DealMind remembers</h2>
                  </div>

                  <button
                    className="link-btn"
                    onClick={() => setActiveTab("timeline")}
                  >
                    View timeline →
                  </button>
                </div>

                <div className="memory-list">
                  {interactions.slice(0, 4).map((item) => (
                    <div className="memory-item" key={item.id}>
                      <div className="memory-icon">✦</div>
                      <div>
                        <div className="memory-date">
                          {formatDate(item.date)}
                        </div>
                        <p>{item.text}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="panel insight-panel">
                <div className="panel-label">AI SIGNALS</div>
                <h2>Deal signals</h2>

                <div className="signal">
                  <div className="signal-icon">!</div>
                  <div>
                    <strong>Pricing pressure</strong>
                    <span>Customer believes pricing is too high.</span>
                  </div>
                </div>

                <div className="signal">
                  <div className="signal-icon">↔</div>
                  <div>
                    <strong>Competitive evaluation</strong>
                    <span>Salesforce is being evaluated.</span>
                  </div>
                </div>

                <div className="signal">
                  <div className="signal-icon">⌁</div>
                  <div>
                    <strong>Technical blocker</strong>
                    <span>CTO is concerned about integration risk.</span>
                  </div>
                </div>
              </div>
            </section>

            <section className="panel add-panel">
              <div className="panel-header">
                <div>
                  <p className="panel-label">CAPTURE MEMORY</p>
                  <h2>Add a new interaction</h2>
                </div>

                <span className="hindsight-badge">
                  Hindsight retain()
                </span>
              </div>

              <textarea
                value={newInteraction}
                onChange={(e) => setNewInteraction(e.target.value)}
                placeholder="Example: The customer asked for a proof of concept before signing."
              />

              <button
                className="primary-btn"
                onClick={addInteraction}
                disabled={loading}
              >
                {loading ? "Saving..." : "Save to Deal Memory"}
              </button>
            </section>
          </>
        )}

        {activeTab === "timeline" && (
          <section className="panel full-panel">
            <div className="panel-header">
              <div>
                <p className="panel-label">DEAL HISTORY</p>
                <h2>Interaction Timeline</h2>
              </div>

              <span className="hindsight-badge">Persistent memory</span>
            </div>

            <div className="timeline">
              {interactions.map((item) => (
                <div className="timeline-item" key={item.id}>
                  <div className="timeline-dot"></div>

                  <div className="timeline-card">
                    <div className="memory-date">
                      {formatDate(item.date)}
                    </div>
                    <p>{item.text}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {activeTab === "memory" && (
          <section className="panel full-panel">
            <div className="panel-header">
              <div>
                <p className="panel-label">HINDSIGHT RECALL</p>
                <h2>Ask DealMind about this deal</h2>
              </div>
            </div>

            <div className="ask-box">
              <input
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask something like: What pricing concern does this customer have?"
              />

              <button
                className="primary-btn"
                onClick={askDeal}
                disabled={loading}
              >
                {loading ? "Searching..." : "Ask DealMind"}
              </button>
            </div>

            {memories.length > 0 && (
              <div className="recall-results">
                <div className="panel-label">RECALLED FROM HINDSIGHT</div>

                {memories.map((memory, index) => (
                  <div className="recall-card" key={index}>
                    <div className="recall-type">
                      {memory.type || "memory"}
                    </div>
                    <p>{memory.text}</p>
                  </div>
                ))}
              </div>
            )}

            {memories.length === 0 && !loading && (
              <div className="empty-state">
                <div className="empty-icon">✦</div>
                <h3>Ask a question about ACME Corp</h3>
                <p>
                  DealMind will retrieve relevant information from persistent
                  Hindsight memory.
                </p>
              </div>
            )}
          </section>
        )}

        {activeTab === "intelligence" && (
          <section className="panel full-panel">
            <div className="panel-header">
              <div>
                <p className="panel-label">HINDSIGHT REFLECT</p>
                <h2>Meeting Intelligence</h2>
              </div>

              <span className="hindsight-badge">
                AI + Persistent Memory
              </span>
            </div>

            {!answer ? (
              <div className="prepare-empty">
                <div className="sparkle">✦</div>
                <h3>Ready to prepare your meeting</h3>

                <p>
                  DealMind will combine everything it remembers about ACME
                  Corp and generate a focused meeting brief.
                </p>

                <button className="primary-btn" onClick={prepareMeeting}>
                  Prepare Meeting Brief
                </button>
              </div>
            ) : (
              <div className="ai-answer">
                <div className="ai-answer-header">
                  <div className="ai-avatar">✦</div>

                  <div>
                    <strong>DealMind</strong>
                    <span>Generated from live Hindsight memory</span>
                  </div>
                </div>

                <div className="answer-content">
                  {answer.split("\n").map((line, index) => {
                    if (!line.trim()) {
                      return (
                        <div className="answer-space" key={index}></div>
                      );
                    }

                    if (line.startsWith("###")) {
                      return (
                        <h3 key={index}>
                          {line.replace(/^###\s*/, "")}
                        </h3>
                      );
                    }

                    if (line.startsWith("####")) {
                      return (
                        <h4 key={index}>
                          {line
                            .replace(/^####\s*/, "")
                            .replace(/\*\*/g, "")}
                        </h4>
                      );
                    }

                    if (line.trim().startsWith("*")) {
                      return (
                        <p className="answer-bullet" key={index}>
                          {line
                            .replace(/^\s*\*\s*/, "")
                            .replace(/\*\*/g, "")}
                        </p>
                      );
                    }

                    if (/^\d+\./.test(line.trim())) {
                      return (
                        <p className="answer-bullet" key={index}>
                          {line.replace(/\*\*/g, "")}
                        </p>
                      );
                    }

                    return (
                      <p key={index}>
                        {line.replace(/\*\*/g, "")}
                      </p>
                    );
                  })}
                </div>
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
