import { Cpu, Circle } from "lucide-react";

export default function Navbar({
  backendOnline,
}) {
  return (
    <header className="fixed left-0 right-0 top-0 z-50 px-4 pt-4 sm:px-6">
      <div className="glass mx-auto flex max-w-7xl items-center justify-between rounded-2xl px-4 py-3 shadow-2xl shadow-black/20 sm:px-6">

        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-blue-400/20 bg-blue-500/10">
            <Cpu
              size={18}
              className="text-blue-400"
            />
          </div>

          <div>
            <p className="text-sm font-semibold tracking-[0.18em] text-white">
              J.A.R.V.I.S.
            </p>

            <p className="text-[9px] tracking-[0.25em] text-slate-500">
              INTELLIGENT SYSTEM
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Circle
            size={8}
            fill="currentColor"
            className={
              backendOnline
                ? "text-emerald-400"
                : "text-red-400"
            }
          />

          <span className="text-[10px] font-medium tracking-[0.18em] text-slate-400">
            {backendOnline
              ? "SYSTEM ONLINE"
              : "OFFLINE"}
          </span>
        </div>

      </div>
    </header>
  );
}