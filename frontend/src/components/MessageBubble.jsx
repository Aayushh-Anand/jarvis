export default function MessageBubble({
  role,
  content,
}) {
  const isUser = role === "user";

  return (
    <div
      className={`flex ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >
      <div
        className={`max-w-[85%] sm:max-w-[70%] ${
          isUser
            ? "rounded-2xl rounded-br-md border border-blue-400/15 bg-blue-500/10"
            : "rounded-2xl rounded-bl-md border border-violet-400/10 bg-slate-900/60"
        } px-4 py-3`}
      >
        <p className="mb-1 text-[9px] font-semibold tracking-[0.2em] text-slate-500">
          {isUser ? "YOU" : "JARVIS"}
        </p>

        <p className="whitespace-pre-wrap text-sm leading-6 text-slate-200">
          {content}
        </p>
      </div>
    </div>
  );
}