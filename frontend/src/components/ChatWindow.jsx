import { useEffect, useRef } from "react";

import MessageBubble from "./MessageBubble";

export default function ChatWindow({
  messages,
  loading,
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  return (
    <div className="glass-strong flex h-[360px] flex-col rounded-3xl p-4 sm:h-[400px]">

      <div className="mb-4 flex items-center justify-between border-b border-white/5 pb-3">
        <div>
          <p className="text-[10px] font-semibold tracking-[0.25em] text-slate-500">
            CONVERSATION
          </p>

          <p className="mt-1 text-xs text-slate-600">
            J.A.R.V.I.S. neural interface
          </p>
        </div>

        <span className="text-[9px] tracking-[0.18em] text-slate-600">
          LIVE
        </span>
      </div>

      <div className="flex-1 space-y-3 overflow-y-auto pr-1">

        {messages.length === 0 && (
          <div className="flex h-full items-center justify-center">
            <div className="text-center">
              <p className="text-sm text-slate-500">
                Conversation initialized.
              </p>

              <p className="mt-1 text-xs text-slate-700">
                Ask JARVIS something.
              </p>
            </div>
          </div>
        )}

        {messages.map((message) => (
          <MessageBubble
            key={message.id}
            role={message.role}
            content={message.content}
          />
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="rounded-2xl rounded-bl-md border border-violet-400/10 bg-slate-900/60 px-4 py-3">
              <div className="flex gap-1">
                <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-blue-400" />
                <span
                  className="h-1.5 w-1.5 animate-bounce rounded-full bg-indigo-400"
                  style={{
                    animationDelay: "100ms",
                  }}
                />
                <span
                  className="h-1.5 w-1.5 animate-bounce rounded-full bg-violet-400"
                  style={{
                    animationDelay: "200ms",
                  }}
                />
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}