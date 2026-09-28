import { useEffect, useState } from "react";
import "./App.css";

const API =
  import.meta.env.VITE_API_URL || "https://dealmind-api.onrender.com";

const DEAL_ID = "acme-001";

function App() {
  const [deal, setDeal] = useState(null);
  const [loading, setLoading] = useState(true);
  const [preparing, setPreparing] = useState(false);
  const [answer, setAnswer] = useState("");
  const [error, setError] = useState("");

  const [interaction, setInteraction] = useState("");
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState("");

  useEffect(() => {
    loadDeal();
  }, []);

  async function loadDeal() {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(`${API}/api/deals/${DEAL_ID}`);

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
      }

      const data = await response.json();
      setDeal(data);
    } catch (err) {
      console.error(err);
      setError(
        "Backend is not reachable. Please try again in a few seconds."
      );
    } finally {
      setLoading(false);
    }
  }

  async function prepareMeeting() {
    try {
      setPreparing(true);
      setError("");
      setAnswer("");

      const response = await fetch(`${API}/api/deals/reflect`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          deal_id: DEAL_ID,
          question:
            "Prepare me for my next meeting with ACME Corp. Use only verified deal memories. Do not invent dates or events.",
        }),
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || `Backend returned ${response.status}`);
      }

      const data = await response.json();
      setAnswer(data.answer || "No meeting intelligence returned.");
    } catch (err) {
      console.error(err);
      setError("Failed to generate meeting intelligence.");
    } finally {
      setPreparing(false);
    }
  }

  async function saveInteraction() {
    if (!interaction.trim()) {
      return;
    }

    try {
      setSaving(true);
      setSaveMessage("");
      setError("");

      const response = await fetch(`${API}/api/interactions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          deal_id: DEAL_ID,
          interaction: interaction.trim(),
        }),
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || `Backend returned ${response.status}`);
      }

      setInteraction("");
      setSaveMessage("Interaction saved to Hindsight memory.");

      setTimeout(() => {
        setSaveMessage("");
      }, 3000);
    } catch (err) {
      console.error(err);
      setError("Failed to save interaction.");
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <div className="loading-screen">
        <div>
          <div className="loading-icon">✦</div>
          <h1>Loading DealMind...</h1>
          <p>Connecting to live deal intelligence.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">✦</div>
          <div>
            <div className="brand-name">DealMind</div>
            <div className="brand-subtitle">
              AI Deal Intelligence
            </div>
          </div>
        </div>

        <div className="connection">
          <span className="connection-dot"></span>
          Hindsight Connected
        </div>
      </header>

      <main className="main">
        {error && (
          <div className="error-box">
            <strong>Connection issue:</strong> {error}
          </div>
        )}

        <section className="hero">
          <div>
            <div className="eyebrow">DEAL INTELLIGENCE</div>

            <h1>{deal?.company || "ACME Corp"}</h1>

            <p>
              {deal?.job_title ||
                deal?.description ||
                "Enterprise Analytics Platform"}{" "}
              • {DEAL_ID}
            </p>
          </div>

          <button
            className="prepare-button"
            onClick={prepareMeeting}
            disabled={preparing}
          >
            ✦ {preparing ? "Preparing..." : "Prepare Me for Meeting"}
          </button>
        </section>

        <section className="content-grid">
          <div className="left-column">
            <div className="card">
              <div className="card-title">
                <span>DEAL OVERVIEW</span>
              </div>

              <div className="overview-grid">
                <div>
                  <span className="label">Company</span>
                  <strong>{deal?.company || "ACME Corp"}</strong>
                </div>

                <div>
                  <span className="label">Deal ID</span>
                  <strong>{DEAL_ID}</strong>
                </div>

                <div>
                  <span className="label">Product</span>
                  <strong>
                    {deal?.product || "Enterprise Analytics Platform"}
                  </strong>
                </div>

                <div>
                  <span className="label">Memory</span>
                  <strong>Hindsight</strong>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="card-title">
                <span>ADD INTERACTION</span>
                <span className="memory-badge">PERSISTENT MEMORY</span>
              </div>

              <p className="card-description">
                Add a real customer interaction. DealMind stores it in
                Hindsight and uses it in future meeting preparation.
              </p>

              <textarea
                value={interaction}
                onChange={(e) => setInteraction(e.target.value)}
                placeholder="Example: The customer asked for a security review before signing."
              />

              <button
                className="save-button"
                onClick={saveInteraction}
                disabled={saving || !interaction.trim()}
              >
                {saving ? "Saving..." : "Save to Hindsight"}
              </button>

              {saveMessage && (
                <div className="success-message">{saveMessage}</div>
              )}
            </div>
          </div>

          <div className="right-column">
            <div className="card intelligence-card">
              <div className="card-title">
                <span>HINDSIGHT REFLECT</span>
                <span className="live-badge">LIVE</span>
              </div>

              <div className="intelligence-header">
                <div className="spark">✦</div>

                <div>
                  <h2>Meeting Intelligence</h2>
                  <p>AI + Persistent Memory</p>
                </div>
              </div>

              <div className="answer">
                {answer ? (
                  <div className="markdown-text">
                    {answer.split("\n").map((line, index) => (
                      <p key={index}>
                        {line || "\u00A0"}
                      </p>
                    ))}
                  </div>
                ) : (
                  <div className="empty-state">
                    <div className="empty-icon">✦</div>

                    <h3>Ready for your next meeting?</h3>

                    <p>
                      Click <strong>Prepare Me for Meeting</strong> to
                      generate a personalized brief from ACME Corp's
                      accumulated Hindsight memory.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer>
        DealMind • Powered by Hindsight persistent memory
      </footer>
    </div>
  );
}

export default App;