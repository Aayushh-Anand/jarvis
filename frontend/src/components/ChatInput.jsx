import { Send } from "lucide-react";
import { useState } from "react";

import VoiceButton from "./VoiceButton";

export default function ChatInput({
  onSend,
  loading,
}) {
  const [message, setMessage] = useState("");
  const [listening, setListening] = useState(false);

  function submitMessage(event) {
    event.preventDefault();

    const trimmed = message.trim();

    if (!trimmed || loading) {
      return;
    }

    onSend(trimmed);
    setMessage("");
  }

  function handleKeyDown(event) {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();

      submitMessage(event);
    }
  }

  function handleVoiceClick() {
    setListening((current) => !current);

    setTimeout(() => {
      setListening(false);
    }, 1200);
  }

  return (
    <form
      onSubmit={submitMessage}
      className="glass-strong flex items-center gap-3 rounded-3xl p-2 pl-5"
    >
      <input
        type="text"
        value={message}
        onChange={(event) =>
          setMessage(event.target.value)
        }
        onKeyDown={handleKeyDown}
        placeholder="Ask JARVIS anything..."
        disabled={loading}
        className="min-w-0 flex-1 bg-transparent py-3 text-sm text-white outline-none placeholder:text-slate-600"
      />

      <VoiceButton
        listening={listening}
        onClick={handleVoiceClick}
      />

      <button
        type="submit"
        disabled={
          loading ||
          !message.trim()
        }
        className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-500/15 text-blue-300 transition hover:bg-blue-500/25 disabled:cursor-not-allowed disabled:opacity-30"
        aria-label="Send message"
      >
        <Send size={18} />
      </button>
    </form>
  );
}