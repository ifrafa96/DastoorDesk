"use client";

import React from "react";
import LogoIntro from "./LogoIntro";

export default function ClientWrapper({ children }: { children: React.ReactNode }) {
  return <LogoIntro>{children}</LogoIntro>;
}