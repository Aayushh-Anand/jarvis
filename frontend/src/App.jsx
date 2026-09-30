import { useEffect, useRef, useState } from "react";

import { ReactLenis } from "lenis/react";
import "lenis/dist/lenis.css";

import Navbar from "./components/Navbar";
import JarvisOrb from "./components/JarvisOrb";
import StatusIndicator from "./components/StatusIndicator";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";

import {
  checkBackend,
  sendMessage,
} from "./services/api";

function App() {
  const [backendOnline, setBackendOnline] =
    useState(false);

  const [status, setStatus] =
    useState("ready");

  const [loading, setLoading] =
    useState(false);

  const [messages, setMessages] =
    useState([]);

  const conversationId =
    useRef(
      `web-${crypto.randomUUID()}`
    );

  useEffect(() => {
    async function initialize() {
      const online =
        await checkBackend();

      setBackendOnline(online);
    }

    initialize();

    const interval =
      setInterval(async () => {
        const online =
          await checkBackend();

        setBackendOnline(online);
      }, 10000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  async function handleSend(message) {
    if (!backendOnline) {
      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "model",
          content:
            "Backend is offline. Please start the JARVIS FastAPI server first.",
        },
      ]);

      return;
    }

    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: message,
    };

    setMessages((current) => [
      ...current,
      userMessage,
    ]);

    setLoading(true);
    setStatus("thinking");

    try {
      const response =
        await sendMessage(
          conversationId.current,
          message
        );

      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "model",
          content:
            response ||
            "I received your request, but no response was returned.",
        },
      ]);

      setStatus("ready");
    } catch (error) {
      console.error(error);

      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "model",
          content:
            "I couldn't connect to the JARVIS backend.",
        },
      ]);

      setStatus("error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <ReactLenis root>

      <div className="min-h-screen overflow-hidden">

        <Navbar
          backendOnline={backendOnline}
        />

        <main className="mx-auto flex min-h-screen max-w-5xl flex-col px-4 pb-10 pt-28 sm:px-6">

          {/* Hero */}
          <section className="flex flex-col items-center">

            <p className="mb-3 text-[10px] font-semibold tracking-[0.45em] text-blue-400/70">
              JUST A RATHER VERY INTELLIGENT SYSTEM
            </p>

            <h1 className="text-center text-3xl font-semibold tracking-tight text-white sm:text-5xl">
              J.A.R.V.I.S.
            </h1>

            <p className="mt-3 max-w-md text-center text-sm leading-6 text-slate-500">
              Your personal AI interface for
              conversations, productivity and
              computer interaction.
            </p>

            <div className="mt-8">
              <JarvisOrb
                status={status}
              />
            </div>

            <StatusIndicator
              status={status}
            />

          </section>

          {/* Interface */}
          <section className="mx-auto mt-10 w-full max-w-3xl">

            <ChatWindow
              messages={messages}
              loading={loading}
            />

            <div className="mt-4">
              <ChatInput
                onSend={handleSend}
                loading={loading}
              />
            </div>

          </section>

          {/* Footer status */}
          <footer className="mt-auto pt-12 text-center">

            <p className="text-[9px] tracking-[0.3em] text-slate-700">
              J.A.R.V.I.S. • LOCAL CONTROL INTERFACE
            </p>

            <p className="mt-2 text-[9px] text-slate-800">
              Manual launch only
            </p>

          </footer>

        </main>

      </div>

    </ReactLenis>
  );
}

export default App;