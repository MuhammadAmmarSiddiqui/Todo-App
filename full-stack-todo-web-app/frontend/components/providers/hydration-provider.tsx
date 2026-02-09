'use client';

import { ReactNode, useEffect, useState } from 'react';

export function HydrationProvider({ children }: { children: ReactNode }) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    // Render nothing during hydration to avoid mismatches
    return null;
  }

  return <>{children}</>;
}