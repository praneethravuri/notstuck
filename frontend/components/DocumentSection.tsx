"use client";

import { useState } from "react";
import { Database, FileSearch, File, Search } from "lucide-react";
import { Input } from "./ui/input";

interface PdfFile {
  name: string;
}

interface DocumentsSectionProps {
  files: PdfFile[];
}

export const DocumentsSection = ({ files }: DocumentsSectionProps) => {
  const [searchQuery, setSearchQuery] = useState("");

  // Filter files based on search query
  const filteredFiles = files.filter((file) =>
    file.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div>
      <div className="flex items-center gap-3 mb-6">
        <div className="h-10 w-10 rounded-lg bg-green-500/10 flex items-center justify-center">
          <Database className="h-4 w-4 text-green-600" />
        </div>
        <div>
          <h2 className="text-base font-medium text-gray-200">Knowledge Base</h2>
        </div>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
        <Input
          type="text"
          placeholder="Search documents..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10 bg-stone-800 border-gray-700 focus:ring-blue-500/20 focus:border-blue-500/40"
        />
      </div>

      <div className="space-y-2 max-h-64 overflow-y-auto pr-2">
        {filteredFiles.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-8 text-gray-400">
            <FileSearch className="h-8 w-8 mb-2 opacity-50" />
            <p className="text-sm">No matching files found</p>
          </div>
        ) : (
          filteredFiles.map((file, index) => (
            <div
              key={index}
              className="group flex items-center gap-3 p-2 rounded-lg hover:bg-stone-800 transition-colors"
            >
              <div className="h-8 w-8 rounded bg-stone-800 group-hover:bg-stone-700 flex items-center justify-center">
                <File className="h-4 w-4 text-green-600" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-300 truncate">{file.name}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
