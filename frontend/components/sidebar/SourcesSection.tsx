// SourcesSection.tsx
"use client";

import { FileText } from "lucide-react";

interface SourcesSectionProps {
  relevantChunks: string[];
}

export const SourcesSection = ({ relevantChunks }: SourcesSectionProps) => {
  return (
    <div className="p-4 h-1/2 border-t border-zinc-800 overflow-y-auto">
      <h2 className="text-sm font-semibold mb-4 text-gray-200 flex items-center space-x-2">
        <FileText className="h-4 w-4 text-green-600" />
        <span>Active Context Sources</span>
      </h2>

      {relevantChunks.length === 0 ? (
        <div className="text-sm text-gray-400 px-3 py-2">No active sources</div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {relevantChunks.map((chunk, index) => (
            <div key={index} className="bg-stone-900 p-4 rounded-lg shadow">
              <p className="text-sm text-gray-200">{chunk}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
