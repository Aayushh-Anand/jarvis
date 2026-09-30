export default function StatusIndicator({
  status,
}) {
  const statusData = {
    ready: {
      label: "READY",
      color: "bg-emerald-400",
      text: "text-emerald-400",
    },

    thinking: {
      label: "THINKING",
      color: "bg-blue-400",
      text: "text-blue-400",
    },

    listening: {
      label: "LISTENING",
      color: "bg-violet-400",
      text: "text-violet-400",
    },

    speaking: {
      label: "SPEAKING",
      color: "bg-cyan-400",
      text: "text-cyan-400",
    },

    error: {
      label: "ERROR",
      color: "bg-red-400",
      text: "text-red-400",
    },
  };

  const current =
    statusData[status] ||
    statusData.ready;

  return (
    <div className="flex items-center justify-center gap-2">
      <span className="relative flex h-2 w-2">
        <span
          className={`absolute inline-flex h-full w-full animate-ping rounded-full opacity-60 ${current.color}`}
        />

        <span
          className={`relative inline-flex h-2 w-2 rounded-full ${current.color}`}
        />
      </span>

      <span
        className={`text-[10px] font-semibold tracking-[0.25em] ${current.text}`}
      >
        {current.label}
      </span>
    </div>
  );
}