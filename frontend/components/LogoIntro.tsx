"use client";

import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function LogoIntro({ children }: { children: React.ReactNode }) {
  const [showIntro, setShowIntro] = useState(true);

  useEffect(() => {
    // 1. Auto-exit after animation
    const timer = setTimeout(() => setShowIntro(false), 4000);
    
    // 2. Immediate exit on scroll
    const handleScroll = () => {
      if (window.scrollY > 20) setShowIntro(false);
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      clearTimeout(timer);
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <>
      <AnimatePresence>
        {showIntro && (
          <motion.div
            initial={{ opacity: 1 }}
            exit={{ opacity: 0, transition: { duration: 0.8 } }}
            // Change Line 28 to:
            className="fixed inset-0 z-[9999] flex items-center justify-center bg-[radial-gradient(circle_at_center,_#f0fdf4_0%,_#ffffff_100%)] overflow-hidden"
          >
            {/* Background Glow - Matching your Emerald/Cyan UI accents */}
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: [0.2, 0.4, 0.2] }}
              transition={{ duration: 3, repeat: Infinity }}
              className="absolute w-[800px] h-[800px] bg-emerald-200/30 blur-[150px] rounded-full" 
            />

            <div className="relative flex flex-col items-center">
              
              {/* 1. SCALE OF JUSTICE (Emerges from the book) */}
              <motion.div
                initial={{ opacity: 0, y: 50, scale: 0.8 }}
                animate={{ opacity: 1, y: -130, scale: 1 }}
                transition={{ delay: 1.5, duration: 1, ease: "easeOut" }}
                className="absolute text-emerald-600 drop-shadow-[0_0_20px_rgba(16,185,129,0.2)]"
              >
                <svg width="90" height="90" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.2">
                  <path d="M16 16c0 1.1.9 2 2 2s2-.9 2-2H16Z"/><path d="M4 16c0 1.1.9 2 2 2s2-.9 2-2H4Z"/><path d="M12 3v18"/><path d="M3 7h18"/><path d="M6 7l-2 9"/><path d="M6 7l2 9"/><path d="M18 7l-2 9"/><path d="M18 7l2 9"/><path d="M12 7l-3 3"/><path d="M12 7l3 3"/>
                </svg>
              </motion.div>

              {/* 2. THE 3D CONSTITUTION BOOK */}
              <div className="relative w-56 h-72 perspective-1000">
                {/* Emerging Internal Light */}
                <motion.div
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1.6 }}
                  transition={{ delay: 1, duration: 2 }}
                  className="absolute inset-0 z-10 m-auto w-24 h-32 bg-emerald-400 blur-[60px] rounded-full opacity-50"
                />

                {/* Book Pages (Depth) */}
                <div className="absolute inset-0 m-auto w-52 h-68 bg-slate-200 rounded-sm shadow-2xl border-r-4 border-slate-300" />

                {/* Left Cover (Opening) */}
                <motion.div
                  initial={{ rotateY: 0 }}
                  animate={{ rotateY: -145 }}
                  transition={{ delay: 0.5, duration: 2.5, ease: [0.45, 0.05, 0.55, 0.95] }}
                  style={{ transformOrigin: "right", transformStyle: "preserve-3d" }}
                  className="absolute left-0 w-28 h-72 bg-slate-900 border-l-[10px] border-slate-950 rounded-l-lg shadow-[20px_0_40px_rgba(0,0,0,0.5)] z-20 flex items-center justify-center"
                >
                   {/* Gold/Emerald Spine Detail */}
                   <div className="w-20 h-56 border border-emerald-500/10 rounded-sm flex items-center justify-center">
                      <div className="w-1 h-32 bg-emerald-500/20 rounded-full" />
                   </div>
                </motion.div>

                {/* Right Cover */}
                <div className="absolute right-0 w-28 h-72 bg-slate-900 border-r-[10px] border-slate-950 rounded-r-lg shadow-2xl z-20" />
              </div>

              {/* 3. TEXT CONTENT (With Glow) */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 2.2, duration: 0.8 }}
                className="mt-16 text-center"
              >
                <h1 className="text-5xl font-extrabold tracking-[0.1em] text-slate-800 drop-shadow-sm">
                  DASTOOR DESK
                </h1>
                <motion.div 
                  initial={{ width: 0 }}
                  animate={{ width: "100%" }}
                  transition={{ delay: 2.8, duration: 1 }}
                  className="h-[2px] bg-emerald-500/50 mt-2 mx-auto"
                />
                <p className="text-emerald-600 font-medium tracking-[0.5em] text-[10px] mt-3 uppercase opacity-90">
                  Justice Powered by AI
                </p>
              </motion.div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 4. THE MAIN WEBSITE CONTENT */}
      {/* We keep it in a container that prevents scroll while the intro is active */}
      <div className={showIntro ? "h-screen overflow-hidden pointer-events-none" : "min-h-screen relative"}>
        {children}
      </div>

      <style jsx global>{`
        .perspective-1000 {
          perspective: 1000px;
        }
      `}</style>
    </>
  );
}