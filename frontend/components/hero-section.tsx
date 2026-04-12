"use client"

import { motion } from "framer-motion"
import { Scale, BrainCircuit, Activity, FileCheck2, ChevronRight, ShieldAlert } from "lucide-react"

export function HeroSection() {
  return (
    <section className="relative overflow-hidden bg-background py-20 sm:py-32">
      {/* Deep Navy/Neon Background glowing blobs layer */}
      <div className="absolute inset-0 max-w-full overflow-hidden pointer-events-none">
        <div className="absolute -top-[10%] -left-[5%] w-[40%] h-[40%] rounded-full bg-primary/20 blur-[150px]" />
        <div className="absolute top-[30%] -right-[10%] w-[35%] h-[50%] rounded-full bg-accent/15 blur-[150px]" />
      </div>
      
      {/* Precision Grid Pattern */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#00000008_1px,transparent_1px),linear-gradient(to_bottom,#00000008_1px,transparent_1px)] dark:bg-[linear-gradient(to_right,#ffffff08_1px,transparent_1px),linear-gradient(to_bottom,#ffffff08_1px,transparent_1px)] bg-[size:32px_32px] pointer-events-none" />
      
      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          
          <div className="max-w-2xl text-left">
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, ease: "easeOut" }}
              className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-sm font-medium text-primary shadow-sm shadow-primary/20 backdrop-blur-md"
            >
              <Scale className="h-4 w-4" />
              Advanced Legal Assistant
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, ease: "easeOut", delay: 0.1 }}
            >
              <h1 className="text-balance text-4xl font-extrabold tracking-tight sm:text-5xl lg:text-6xl text-foreground">
                Authoritative{" "}
                <span className="bg-gradient-to-r from-primary via-blue-400 to-primary bg-clip-text text-transparent drop-shadow-sm">
                  Your Legal Assistant
                </span>
              </h1>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, ease: "easeOut", delay: 0.2 }}
            >
              <p className="mt-6 text-pretty text-lg sm:text-xl leading-relaxed text-muted-foreground/90 font-light">
                Accelerate legal research and decision-making. Extract critical precedents, analyze case complexity, and synthesize verifiable outcomes with our highly-tuned legal reasoning engine.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0,}}
              animate={{ opacity: 1 }}
              transition={{ duration: 1, ease: "easeOut", delay: 0.4 }}
              className="mt-10 flex flex-wrap items-center gap-4"
            >
              <button className="flex items-center gap-2 rounded-lg bg-primary px-6 py-3 text-sm font-bold text-primary-foreground transition-all hover:bg-primary/90 hover:shadow-lg hover:shadow-primary/40">
                Start Analysis <ChevronRight className="h-4 w-4" />
              </button>
              <button className="flex items-center gap-2 rounded-lg bg-background/50 backdrop-blur border border-border/50 px-6 py-3 text-sm font-medium text-foreground transition-all hover:bg-background/80 hover:border-primary/50">
                View Demo
              </button>
            </motion.div>
          </div>

          {/* Dashboard Glassmorphism Grid */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, ease: "easeOut", delay: 0.3 }}
            className="grid gap-4 sm:grid-cols-2 relative"
          >
            {/* Main Panel */}
            <div className="sm:col-span-2 rounded-2xl border border-white/60 dark:border-white/10 bg-white/40 dark:bg-black/40 backdrop-blur-2xl p-6 shadow-xl dark:shadow-2xl shadow-black/5 relative overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
              <div className="flex justify-between items-center mb-4">
                <div className="flex items-center gap-2 text-sm font-medium text-primary">
                  <BrainCircuit className="h-4 w-4" /> Real-time Case Analysis
                </div>
                <span className="flex h-2 w-2 rounded-full bg-green-500 animate-pulse" />
              </div>
              <div className="space-y-3">
                <div className="h-2 w-3/4 rounded bg-black/5 dark:bg-white/5" />
                <div className="h-2 w-full rounded bg-black/5 dark:bg-white/5" />
                <div className="h-2 w-5/6 rounded bg-black/5 dark:bg-white/5" />
              </div>
              <div className="mt-6 flex items-center justify-between border-t border-black/10 dark:border-white/10 pt-4 text-xs text-muted-foreground">
                <span className="flex items-center gap-1"><ShieldAlert className="h-3 w-3" /> Encrypted Protocol</span>
                <span>Accuracy: 98.4%</span>
              </div>
            </div>

            {/* Sub Panel 1 */}
            <div className="rounded-2xl border border-white/60 dark:border-white/10 bg-white/40 dark:bg-black/40 backdrop-blur-2xl p-5 shadow-lg shadow-black/5 dark:shadow-xl hover:border-accent/50 dark:hover:border-accent/30 transition-colors">
              <div className="mb-3 flex h-8 w-8 items-center justify-center rounded-lg bg-accent/20 text-accent">
                <Activity className="h-4 w-4" />
              </div>
              <h3 className="mb-1 text-sm font-semibold text-foreground">Risk Assessment</h3>
              <p className="text-xs text-muted-foreground">Multi-factor precedent evaluation</p>
            </div>

            {/* Sub Panel 2 */}
            <div className="rounded-2xl border border-white/60 dark:border-white/10 bg-white/40 dark:bg-black/40 backdrop-blur-2xl p-5 shadow-lg shadow-black/5 dark:shadow-xl hover:border-primary/50 dark:hover:border-primary/30 transition-colors">
              <div className="mb-3 flex h-8 w-8 items-center justify-center rounded-lg bg-primary/20 text-primary">
                <FileCheck2 className="h-4 w-4" />
              </div>
              <h3 className="mb-1 text-sm font-semibold text-foreground">Citation Validation</h3>
              <p className="text-xs text-muted-foreground">Automated statute verification</p>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  )
}
