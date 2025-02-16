"use client";
import React from "react";
import { Loader2 } from "lucide-react";

interface LoadingPageProps {
  error?: string | null;
}

/**
 * Full-screen loading overlay with optional error text.
 */
export default function LoadingPage({ error }: LoadingPageProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-stone-950 text-gray-50">
      <Loader2 className="h-10 w-10 animate-spin text-green-500 mb-4" />
      <p>Starting up the app. Please wait...</p>
      {error && <p className="text-red-400 mt-2 text-sm">{error}</p>}
    </div>
  );
}
