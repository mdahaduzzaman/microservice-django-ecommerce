"use client";

import { QueryClientProvider } from "@tanstack/react-query";
import React from "react";
import { getQueryClient } from "./get-query-client";

function QueryProvider({ children }: { children: React.ReactNode }) {
  const queryClient = getQueryClient();
  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

export default QueryProvider;
