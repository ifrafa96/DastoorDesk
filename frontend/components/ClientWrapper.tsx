"use client";

import React from "react";
import LogoIntro from "./LogoIntro";
import { CursorOrb } from "./cursor-orb";

export default function ClientWrapper({ children }: { children: React.ReactNode }) {
  return (
    <>
      <CursorOrb />
      <LogoIntro>{children}</LogoIntro>
    </>
  );
}