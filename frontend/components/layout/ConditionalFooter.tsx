"use client";

import { usePathname } from "next/navigation";
import { Footer } from "./Footer";

export function ConditionalFooter() {
  const pathname = usePathname();

  // Hide footer on the /generate page
  if (pathname === "/generate") {
    return null;
  }

  return <Footer />;
}
