import { useEffect, useRef, useState } from "react";
import "./ChatWidget.css";

const suggestions = [
  "Suggest a project",
  "What skills should I learn?",
  "Give me a roadmap",
];

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hi! I'm your BuildWise AI project mentor. ✨ Ask me about project ideas, skills, roadmaps, or internship preparation.",
    },
  ]);
  const endRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, busy, open]);

  async function sendMessage(text = message) {
    const clean = text.trim();
    if (!clean || busy) return;

    setMessages((old) => [...old, { role: "user", text: clean }]);
    setMessage("");
    setBusy(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: clean }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Request failed");

      setMessages((old) => [...old, {
        role: "assistant",
        text: data.reply || "I couldn't generate a reply. Please try again.",
      }]);
    } catch {
      setMessages((old) => [...old, {
        role: "assistant",
        text: "I couldn't connect to the chatbot service. Please check that the Python API is running, then try again.",
      }]);
    } finally {
      setBusy(false);
      inputRef.current?.focus();
    }
  }

  return (
    <div className="bw-chat-root">
      {open && (
        <section className="bw-chat-panel" aria-label="BuildWise AI chat">
          <header className="bw-chat-header">
            <div className="bw-chat-avatar">✦</div>
            <div className="bw-chat-heading">
              <strong>BuildWise AI</strong>
              <span><i /> Your project mentor</span>
            </div>
            <button
              className="bw-chat-close"
              onClick={() => setOpen(false)}
              aria-label="Close chat"
            >×</button>
          </header>

          <div className="bw-chat-intro">
            <span className="bw-chat-label">YOUR AI COMPANION</span>
            <p>Let's turn your ideas into something real.</p>
          </div>

          <div className="bw-chat-messages" aria-live="polite">
            {messages.map((item, index) => (
              <div
                key={`${index}-${item.role}`}
                className={`bw-chat-message ${item.role}`}
              >
                {item.role === "assistant" && (
                  <span className="bw-message-avatar">✦</span>
                )}
                <div className="bw-message-bubble">{item.text}</div>
              </div>
            ))}
            {busy && (
              <div className="bw-chat-message assistant">
                <span className="bw-message-avatar">✦</span>
                <div className="bw-message-bubble bw-typing">
                  <span /><span /><span />
                </div>
              </div>
            )}
            <div ref={endRef} />
          </div>

          {messages.length === 1 && (
            <div className="bw-chat-suggestions">
              <span>TRY ASKING</span>
              {suggestions.map((suggestion) => (
                <button
                  key={suggestion}
                  disabled={busy}
                  onClick={() => sendMessage(suggestion)}
                >{suggestion}<span>↗</span></button>
              ))}
            </div>
          )}

          <form
            className="bw-chat-form"
            onSubmit={(event) => {
              event.preventDefault();
              sendMessage();
            }}
          >
            <input
              ref={inputRef}
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              placeholder="Ask me anything..."
              aria-label="Your message"
              maxLength={2000}
              disabled={busy}
            />
            <button
              type="submit"
              disabled={!message.trim() || busy}
              aria-label="Send message"
            >↗</button>
          </form>
          <p className="bw-chat-footnote">Powered by BuildWise AI · Rule-based assistant</p>
        </section>
      )}

      <button
        className={`bw-chat-launcher ${open ? "is-open" : ""}`}
        onClick={() => setOpen((value) => !value)}
        aria-label={open ? "Close BuildWise AI chat" : "Open BuildWise AI chat"}
        aria-expanded={open}
      >
        {open ? <span className="bw-launcher-close">×</span> : (
          <>
            <span className="bw-launcher-icon">✦</span>
            <span className="bw-launcher-text">Ask BuildWise</span>
            <span className="bw-launcher-sparkle">✧</span>
          </>
        )}
      </button>
    </div>
  );
}
