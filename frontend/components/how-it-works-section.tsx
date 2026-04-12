"use client"

import { motion } from "framer-motion"
import { MessageSquare, Brain, FileText, CheckCircle } from "lucide-react"

const steps = [
  {
    icon: MessageSquare,
    title: "Initial Query Processing",
    description: "Input your legal situation in natural language. Our system parses the intent without requiring legal jargon.",
  },
  {
    icon: Brain,
    title: "Neural Precedent Matching",
    description: "The AI cross-references your scenario against a vast database of localized statutes and case law.",
  },
  {
    icon: FileText,
    title: "Synthesis & Extraction",
    description: "Receive a structured analysis detailing applicable laws, risks, and recommended procedural steps.",
  },
  {
    icon: CheckCircle,
    title: "Actionable Directives",
    description: "Follow clear evidence collection and authority engagement protocols tailored to your case.",
  },
]

export function HowItWorksSection() {
  return (
    <section id="how-it-works" className="relative border-t border-white/5 bg-background py-20 sm:py-32 overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom,var(--accent),transparent_50%)] opacity-5 pointer-events-none" />
      
      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6 }}
          className="mx-auto max-w-2xl text-center"
        >
          <div className="inline-flex items-center gap-2 rounded-full border border-black/5 dark:border-white/10 bg-black/5 dark:bg-white/5 px-3 py-1 mb-4 text-xs font-semibold text-muted-foreground uppercase tracking-widest backdrop-blur-md">
            Methodology
          </div>
          <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl lg:text-5xl">
            System Workflow
          </h2>
          <p className="mt-4 text-lg text-muted-foreground/80 font-light">
            A secure, multi-stage protocol for accurate legal assessment
          </p>
        </motion.div>

        <div className="mt-16 grid gap-8 sm:grid-cols-2 lg:grid-cols-4 relative">
          <div className="absolute top-8 left-[12.5%] right-[12.5%] hidden h-px bg-gradient-to-r from-transparent via-primary/30 to-transparent lg:block" />
          
          {steps.map((step, index) => {
            const Icon = step.icon
            return (
              <motion.div 
                key={index} 
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-50px" }}
                transition={{ duration: 0.5, delay: index * 0.15 }}
                className="relative text-center group"
              >
                <div className="relative mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl border border-white/60 dark:border-white/10 bg-white/40 dark:bg-black/50 backdrop-blur-xl text-primary shadow-lg shadow-black/5 dark:shadow-black/50 transition-all duration-300 group-hover:-translate-y-1 hover:bg-white/60 dark:hover:bg-black/70 hover:border-white/80 dark:group-hover:border-primary/50 group-hover:shadow-xl group-hover:shadow-primary/20 dark:group-hover:shadow-primary/30">
                  <Icon className="h-7 w-7" />
                  <span className="absolute -right-2 -top-2 flex h-6 w-6 items-center justify-center rounded-full border border-white/80 dark:border-white/10 bg-accent text-xs font-bold text-accent-foreground shadow-sm">
                    {index + 1}
                  </span>
                </div>
                <h3 className="mb-2 text-base font-bold text-foreground">{step.title}</h3>
                <p className="text-sm leading-relaxed text-muted-foreground/80 font-light px-2">{step.description}</p>
              </motion.div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
