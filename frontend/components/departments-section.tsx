"use client"

import { motion, Variants } from "framer-motion"
import { DepartmentCard } from "@/components/department-card"
import { legalDepartments } from "@/lib/legal-departments"

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
}

const itemVariants: Variants = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 100 } }
}

export function DepartmentsSection() {
  return (
    <section id="departments" className="py-20 sm:py-32 relative bg-background border-t border-black/5 dark:border-white/5">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,var(--primary),transparent_50%)] opacity-5 pointer-events-none" />
      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6 }}
          className="mx-auto max-w-2xl text-center"
        >
          <div className="inline-flex items-center gap-2 rounded-full border border-black/5 dark:border-white/10 bg-black/5 dark:bg-white/5 px-3 py-1 mb-4 text-xs font-semibold text-muted-foreground uppercase tracking-widest backdrop-blur-md">
            Practice Areas
          </div>
          <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl lg:text-5xl">
            Legal Jurisdictions
          </h2>
          <p className="mt-4 text-pretty text-lg text-muted-foreground/80 font-light">
            Select a specialized module to initiate advanced query processing. Our models are individually trained on specific statutory frameworks.
          </p>
        </motion.div>

        <motion.div 
          variants={containerVariants}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: "-50px" }}
          className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-4"
        >
          {legalDepartments.map((department) => (
            <motion.div key={department.id} variants={itemVariants} className="h-full">
              <DepartmentCard department={department} />
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}
