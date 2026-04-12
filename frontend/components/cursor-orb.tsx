"use client"

import { useEffect, useState } from "react"
import { motion, useMotionValue, useSpring } from "framer-motion"

export function CursorOrb() {
  const [isVisible, setIsVisible] = useState(false)
  const cursorX = useMotionValue(-100)
  const cursorY = useMotionValue(-100)

  // Spring physics for snappy, fast movement
  const springConfig = { damping: 20, stiffness: 300, mass: 0.2 }
  const x = useSpring(cursorX, springConfig)
  const y = useSpring(cursorY, springConfig)

  // Trailing glow spring physics
  const trailingX = useSpring(cursorX, { damping: 25, stiffness: 120 })
  const trailingY = useSpring(cursorY, { damping: 25, stiffness: 120 })

  useEffect(() => {
    // Only show on desktop devices with fine pointers
    if (window.matchMedia("(pointer: coarse)").matches) {
      return
    }
    
    setIsVisible(true)

    const moveCursor = (e: PointerEvent) => {
      cursorX.set(e.clientX - 16) // Offset by half width/height
      cursorY.set(e.clientY - 16)
    }

    const handleMouseLeave = () => setIsVisible(false)
    const handleMouseEnter = () => setIsVisible(true)

    window.addEventListener("pointermove", moveCursor)
    document.addEventListener("mouseleave", handleMouseLeave)
    document.addEventListener("mouseenter", handleMouseEnter)

    return () => {
      window.removeEventListener("pointermove", moveCursor)
      document.removeEventListener("mouseleave", handleMouseLeave)
      document.removeEventListener("mouseenter", handleMouseEnter)
    }
  }, [cursorX, cursorY])

  if (!isVisible) return null

  return (
    <>
      <motion.div
        className="pointer-events-none fixed top-0 left-0 z-50 h-8 w-8 rounded-full mix-blend-screen"
        style={{ x, y }}
      >
        {/* Core orb */}
        <div className="absolute inset-0 rounded-full bg-primary opacity-60 blur-md shadow-[0_0_20px_var(--primary)]" />
        
        {/* Pulsing subtle rings (neural network vibe) */}
        <motion.div
          animate={{
            scale: [1, 1.5, 1],
            opacity: [0.5, 0.2, 0.5],
            rotate: [0, 90, 360],
          }}
          transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
          className="absolute -inset-2 rounded-full border border-primary/30"
        />
        <motion.div
          animate={{
            scale: [1.2, 0.8, 1.2],
            opacity: [0.3, 0.6, 0.3],
            rotate: [360, 180, 0],
          }}
          transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
          className="absolute -inset-4 rounded-full border border-accent/20 border-dashed"
        />
      </motion.div>
      
      {/* Lagging trailing glow */}
      <motion.div
        className="pointer-events-none fixed top-0 left-0 z-40 h-24 w-24 rounded-full bg-primary/10 blur-3xl mix-blend-screen"
        style={{
          x: trailingX,
          y: trailingY,
          translateX: "-32px",
          translateY: "-32px"
        }}
      />
    </>
  )
}
