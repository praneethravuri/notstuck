"use client";
import React from "react";
import { Loader2, MessageSquare } from "lucide-react";

interface LoadingPageProps {
  error?: string | null;
}

/**
 * Full-screen loading overlay with optional error text.
 */
export default function LoadingPage({ error }: LoadingPageProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 flex flex-col">
      {/* Header - matching chat page */}
      <header className="border-b border-slate-800/50 backdrop-blur-sm bg-slate-950/80 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center shadow-lg shadow-violet-500/20">
              <MessageSquare className="h-5 w-5 text-white" />
            </div>
            <span className="font-bold text-xl text-white">NotStuck</span>
          </div>
        </div>
      </header>

      {/* Loading content */}
      <main className="flex-1 flex flex-col items-center justify-center max-w-5xl w-full mx-auto px-6">
        <Loader2 className="h-12 w-12 animate-spin text-violet-500 mb-4" />
        <p className="text-slate-300 text-lg">Starting up the backend...</p>
        <p className="text-slate-500 text-sm mt-2">Please wait a moment</p>
        {error && (
          <div className="mt-6 p-4 bg-red-500/10 border border-red-500/20 rounded-lg max-w-md">
            <p className="text-red-400 text-sm">{error}</p>
          </div>
        )}
      </main>
    </div>
  );
}
