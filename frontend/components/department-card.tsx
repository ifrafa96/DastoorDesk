"use client"

import Link from "next/link"
import { ArrowRight } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { DepartmentIcon } from "@/components/department-icon"
import type { LegalDepartment } from "@/lib/legal-departments"

interface DepartmentCardProps {
  department: LegalDepartment
}

export function DepartmentCard({ department }: DepartmentCardProps) {
  return (
    <Link href={`/chat/${department.id}`} className="block h-full group outline-none">
      <Card className="h-full bg-white/40 dark:bg-black/40 backdrop-blur-2xl border border-white/60 dark:border-white/10 shadow-xl dark:shadow-lg shadow-black/5 dark:shadow-black/50 transition-all duration-500 ease-out hover:-translate-y-2 hover:shadow-2xl hover:shadow-primary/20 dark:hover:shadow-primary/30 hover:border-sky-300 dark:hover:border-primary/50 relative overflow-hidden">
        
        {/* Neon boundary glow effect on hover */}
        <div className="absolute inset-0 bg-gradient-to-br from-sky-300/30 via-transparent to-pink-300/30 dark:from-primary/20 dark:via-transparent dark:to-accent/20 opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none" />

        <CardHeader className="pb-3 relative z-10">
          <div className={`mb-4 flex h-14 w-14 items-center justify-center rounded-xl border border-black/5 dark:border-white/10 shadow-inner ${department.color} bg-white/50 dark:bg-background/50 backdrop-blur-md transition-colors group-hover:border-sky-300 dark:group-hover:border-primary/50`}>
            <DepartmentIcon name={department.iconName} className="h-7 w-7 text-foreground" />
          </div>
          <CardTitle className="flex items-center justify-between text-xl font-bold tracking-tight text-foreground group-hover:text-primary transition-colors">
            {department.name}
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 text-primary opacity-0 -translate-x-4 transition-all duration-300 group-hover:translate-x-0 group-hover:opacity-100 group-focus-visible:translate-x-0 group-focus-visible:opacity-100">
              <ArrowRight className="h-4 w-4" />
            </div>
          </CardTitle>
          <CardDescription className="text-sm leading-relaxed mt-2 line-clamp-2 text-muted-foreground/80 font-medium">
            {department.description}
          </CardDescription>
        </CardHeader>
        <CardContent className="pt-0 relative z-10">
          <div className="space-y-2 mt-4 pt-4 border-t border-black/5 dark:border-white/5">
            <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">Analysis Models</p>
            <ul className="space-y-2">
              {department.examples.slice(0, 2).map((example, index) => (
                <li
                  key={index}
                  className="flex items-start gap-2 text-xs font-medium text-foreground/70"
                >
                  <span className="mt-1 h-1 w-1 shrink-0 rounded-full bg-accent/70 group-hover:bg-primary shadow-sm shadow-primary/50 transition-colors" />
                  <span className="line-clamp-1">{example}</span>
                </li>
              ))}
            </ul>
          </div>
        </CardContent>
      </Card>
    </Link>
  )
}
