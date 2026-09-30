import { useEffect, useRef } from "react";
import gsap from "gsap";

export default function JarvisOrb({
  status,
}) {
  const orbRef = useRef(null);
  const ringOneRef = useRef(null);
  const ringTwoRef = useRef(null);

  useEffect(() => {
    const orb = orbRef.current;
    const ringOne = ringOneRef.current;
    const ringTwo = ringTwoRef.current;

    if (!orb || !ringOne || !ringTwo) {
      return;
    }

    const context = gsap.context(() => {
      gsap.to(orb, {
        scale: 1.06,
        duration: 2.4,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut",
      });

      gsap.to(ringOne, {
        rotation: 360,
        duration: 14,
        repeat: -1,
        ease: "none",
      });

      gsap.to(ringTwo, {
        rotation: -360,
        duration: 20,
        repeat: -1,
        ease: "none",
      });
    });

    return () => context.revert();
  }, []);

  const active =
    status === "listening" ||
    status === "thinking" ||
    status === "speaking";

  return (
    <div className="relative flex h-64 w-64 items-center justify-center sm:h-72 sm:w-72">

      {/* Outer glow */}
      <div
        className={`absolute h-52 w-52 rounded-full blur-3xl transition-all duration-700 ${
          active
            ? "bg-violet-500/30"
            : "bg-blue-500/20"
        }`}
      />

      {/* Rotating ring */}
      <div
        ref={ringOneRef}
        className="absolute h-56 w-56 rounded-full border border-blue-400/20"
        style={{
          borderTopColor:
            "rgba(96,165,250,0.7)",
          borderRightColor:
            "rgba(139,92,246,0.45)",
        }}
      />

      {/* Second ring */}
      <div
        ref={ringTwoRef}
        className="absolute h-44 w-44 rounded-full border border-violet-400/15"
        style={{
          borderBottomColor:
            "rgba(167,139,250,0.7)",
          borderLeftColor:
            "rgba(96,165,250,0.45)",
        }}
      />

      {/* Orb */}
      <div
        ref={orbRef}
        className="relative flex h-32 w-32 items-center justify-center rounded-full border border-blue-300/30 bg-linear-to-br from-blue-500/20 via-indigo-500/10 to-violet-500/20 shadow-[0_0_80px_rgba(59,130,246,0.2)]"
      >
        <div className="absolute h-20 w-20 rounded-full bg-blue-400/10 blur-xl" />

        <div className="relative h-5 w-5 rounded-full bg-blue-300 shadow-[0_0_35px_rgba(96,165,250,0.95)]" />
      </div>

    </div>
  );
}