"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Loader2, FileCheck, Mic, MicOff, Copy, Check } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { EvidencePanel } from "@/components/evidence-panel";
import { DepartmentIcon } from "@/components/department-icon";
import { askLegalAI } from "@/lib/api";
import ReactMarkdown from "react-markdown";
import type { LegalDepartment } from "@/lib/legal-departments";

interface ChatInterfaceProps {
  department: LegalDepartment;
}

export function ChatInterface({ department }: ChatInterfaceProps) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showEvidence, setShowEvidence] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const handleCopy = (text: string, index: number) => {
    if (typeof navigator !== "undefined") {
      navigator.clipboard.writeText(text);
      setCopiedIndex(index);
      setTimeout(() => setCopiedIndex(null), 2000);
    }
  };

  // 🎤 VOICE INPUT
  const [isListening, setIsListening] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const recognitionRef = useRef<any>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 🔊 VOICE OUTPUT FUNCTION
  const speakText = (text: string) => {
  if ("speechSynthesis" in window) {
    window.speechSynthesis.cancel();

    let cleanText = text
      // 🔥 remove markdown symbols
      .replace(/[#*`>-]/g, "")
      .replace(/\*\*(.*?)\*\*/g, "$1")

      // 🔥 FIX COLONS + STRUCTURE
      .replace(/:/g, ".")          // colon → pause
      .replace(/\n+/g, ". ")       // new lines → pauses

      // 🔥 clean spaces
      .replace(/\s+/g, " ")
      .trim();

    console.log("🔊 CLEAN SPEECH:", cleanText);

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 0.9;
    utterance.pitch = 1;

    window.speechSynthesis.speak(utterance);
  }
};

  // Scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // 🎤 SPEECH RECOGNITION SETUP
  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRecognition =
        (window as any).SpeechRecognition ||
        (window as any).webkitSpeechRecognition;

      if (SpeechRecognition) {
        setSpeechSupported(true);

        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = "en-US";

        recognition.onresult = (event: any) => {
          let transcript = "";

          for (let i = 0; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
          }

          // CLEAN TEXT
          transcript = transcript.replace(/\s+/g, " ").trim();

          const isUrduScript = /[\u0600-\u06FF]/.test(transcript);

          if (!isUrduScript) {
            const lower = transcript.toLowerCase();
            transcript = lower.charAt(0).toUpperCase() + lower.slice(1);
          }

          setInput(transcript);
        };

        recognition.onend = () => setIsListening(false);
        recognition.onerror = () => setIsListening(false);

        recognitionRef.current = recognition;
      }
    }
  }, []);

  // 🎤 TOGGLE VOICE INPUT
  const toggleListening = () => {
    if (!recognitionRef.current) return;

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      const text = input.toLowerCase();

      if (/[؀-ۿ]/.test(text)) {
        recognitionRef.current.lang = "ur-PK";
      } else {
        recognitionRef.current.lang = "en-US";
      }

      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  // 🔥 MAIN CHAT FUNCTION
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = {
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const data = await askLegalAI(input, department.id);

      const botMessage = {
        role: "assistant",
        content: data.answer,
        evidence: data.evidence_list,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error connecting to backend." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-full flex-col">
      {/* Toolbar */}
      <div className="flex justify-end border-b px-4 py-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => setShowEvidence(!showEvidence)}
        >
          <FileCheck className="h-4 w-4 mr-1" />
          Evidence Guide
        </Button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 scroll-smooth bg-gradient-to-b from-background to-secondary/10">
        <div className="mx-auto max-w-3xl space-y-6">
          <AnimatePresence initial={false}>
          {messages.map((message, index) => (
            <motion.div
              initial={{ opacity: 0, y: 10, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.3 }}
              key={index}
              className={`flex w-full mb-4 ${
                message.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`relative px-5 py-4 text-sm md:text-base leading-relaxed ${
                  message.role === "user"
                    ? "max-w-[75%] rounded-2xl bg-primary text-primary-foreground shadow-sm rounded-tr-sm"
                    : "max-w-[90%] rounded-2xl bg-card border border-border/60 shadow-sm text-card-foreground rounded-tl-sm w-full"
                }`}
              >
                <div className="flex flex-col gap-3">
                  <div className="flex justify-between items-start gap-4">
                    <div className="prose prose-sm md:prose-base dark:prose-invert max-w-none text-inherit break-words">
                      <ReactMarkdown
                        components={{
                          h3: ({ ...props }) => <h3 className="font-bold mt-4 mb-2 text-inherit" {...props} />,
                          strong: ({ ...props }) => <strong className="font-semibold text-inherit" {...props} />,
                          li: ({ ...props }) => <li className="ml-4 list-disc text-inherit" {...props} />,
                          p: ({ ...props }) => <p className="mb-3 last:mb-0 text-inherit" {...props} />,
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                    </div>

                    {message.role === "assistant" && (
                      <div className="flex shrink-0 gap-1 mt-1 opacity-60 hover:opacity-100 transition-opacity">
                        <button
                          onClick={() => handleCopy(message.content, index)}
                          className="p-1.5 rounded-md hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
                          title="Copy message"
                        >
                          {copiedIndex === index ? <Check className="h-4 w-4 text-green-500" /> : <Copy className="h-4 w-4" />}
                        </button>
                        <button
                          onClick={() => speakText(message.content)}
                          className="p-1.5 rounded-md hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
                          title="Read aloud"
                        >
                          🔊
                        </button>
                      </div>
                    )}
                  </div>

                  {message.evidence && message.evidence.length > 0 && (
                    <div className="mt-2 pt-3 border-t border-border/50 text-xs text-muted-foreground">
                      <strong className="flex items-center gap-1 mb-2 text-foreground/80"><FileCheck className="h-3 w-3" /> Relevant Sections Mentioned:</strong>
                      <ul className="list-disc ml-5 space-y-1">
                        {message.evidence.map((item: string, i: number) => (
                          <li key={i} className="text-foreground/70">{item}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
          </AnimatePresence>

          {isLoading && (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-start w-full mb-4"
            >
              <div className="max-w-[80%] rounded-2xl bg-card border border-border shadow-sm px-5 py-4 rounded-tl-sm w-32">
                <div className="flex gap-1.5 items-center justify-center py-2 text-primary">
                  <motion.div className="w-2 h-2 rounded-full bg-current opacity-75" animate={{ scale: [1, 1.2, 1], opacity: [0.5, 1, 0.5] }} transition={{ repeat: Infinity, duration: 1, delay: 0 }} />
                  <motion.div className="w-2 h-2 rounded-full bg-current opacity-75" animate={{ scale: [1, 1.2, 1], opacity: [0.5, 1, 0.5] }} transition={{ repeat: Infinity, duration: 1, delay: 0.2 }} />
                  <motion.div className="w-2 h-2 rounded-full bg-current opacity-75" animate={{ scale: [1, 1.2, 1], opacity: [0.5, 1, 0.5] }} transition={{ repeat: Infinity, duration: 1, delay: 0.4 }} />
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="p-4 sm:p-6 bg-gradient-to-t from-background via-background to-transparent border-t-0 pb-6 sm:pb-8">
        <form onSubmit={handleSubmit} className="mx-auto max-w-3xl relative">
          <div className="flex items-end gap-3 rounded-2xl border border-border/80 bg-background/80 backdrop-blur-xl p-2 shadow-lg hover:border-primary/30 transition-all duration-300 focus-within:border-primary/50 focus-within:ring-2 focus-within:ring-primary/20">

            {/* 🎤 MIC */}
            {speechSupported && (
              <Button
                type="button"
                variant="ghost"
                size="icon"
                onClick={toggleListening}
                className={`mb-1 shrink-0 h-10 w-10 transition-colors rounded-xl ${
                  isListening ? "text-red-500 bg-red-500/10 hover:bg-red-500/20" : "text-muted-foreground hover:text-foreground"
                }`}
                disabled={isLoading}
                title={isListening ? "Stop listening" : "Start speaking"}
              >
                {isListening ? (
                  <MicOff className="h-5 w-5 animate-pulse" />
                ) : (
                  <Mic className="h-5 w-5" />
                )}
              </Button>
            )}

            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault(); 
                  handleSubmit(e as any); 
                 }
              }}
              placeholder={
                isListening
                  ? "Listening..."
                  : `Type your ${department.name.toLowerCase()} query here...`
              }
              className="flex-1 min-h-[52px] max-h-32 py-3.5 px-2 resize-none border-0 bg-transparent focus-visible:ring-0 text-sm md:text-base leading-relaxed overflow-hidden disabled:opacity-50"
              disabled={isLoading}
              rows={1}
            />

            <Button 
              type="submit" 
              size="icon"
              disabled={!input.trim() || isLoading}
              className={`mb-1 shrink-0 h-10 w-10 rounded-xl transition-all ${
                input.trim() && !isLoading ? "bg-primary text-primary-foreground shadow-sm hover:scale-105" : "bg-muted text-muted-foreground"
              }`}
            >
              {isLoading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Send className="h-5 w-5 ml-0.5" />
              )}
              <span className="sr-only">Send message</span>
            </Button>

          </div>
        </form>
      </div>

      <EvidencePanel
        departmentId={department.id}
        isOpen={showEvidence}
        onClose={() => setShowEvidence(false)}
      />
    </div>
  );
}