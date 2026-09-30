import { Mic } from "lucide-react";

export default function VoiceButton({
  listening,
  onClick,
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`group relative flex h-14 w-14 items-center justify-center rounded-full border transition-all duration-300 ${
        listening
          ? "border-violet-400/50 bg-violet-500/20 shadow-[0_0_35px_rgba(139,92,246,0.25)]"
          : "border-blue-400/20 bg-blue-500/10 hover:border-blue-400/40 hover:bg-blue-500/15"
      }`}
      aria-label="Voice control"
    >
      {listening && (
        <span className="absolute inset-0 animate-ping rounded-full border border-violet-400/20" />
      )}

      <Mic
        size={20}
        className={
          listening
            ? "relative text-violet-300"
            : "relative text-blue-300"
        }
      />
    </button>
  );
}