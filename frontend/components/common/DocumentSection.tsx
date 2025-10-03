"use client";
import { useState } from "react";
import { Database, FileSearch, File, Search } from "lucide-react";
import { Input } from "../ui/input";
import { ScrollArea } from "../ui/scroll-area";

interface PdfFile {
  name: string;
}

interface DocumentsSectionProps {
  files: PdfFile[];
}

export const DocumentsSection = ({ files }: DocumentsSectionProps) => {
  const [searchQuery, setSearchQuery] = useState("");

  const filteredFiles = files.filter((file) =>
    file.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="bg-slate-900/50 border border-slate-800/50 rounded-xl p-4 backdrop-blur-sm">
      <div className="flex items-center gap-3 mb-4">
        <div className="h-9 w-9 rounded-lg bg-gradient-to-br from-violet-500/20 to-purple-600/20 flex items-center justify-center border border-violet-500/20">
          <Database className="h-4 w-4 text-violet-400" />
        </div>
        <div>
          <h2 className="text-sm font-semibold text-white">Knowledge Base</h2>
          <p className="text-xs text-slate-400">{files.length} documents</p>
        </div>
      </div>
      <div className="relative mb-3">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
        <Input
          type="text"
          placeholder="Search documents..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10 bg-slate-800/50 border-slate-700/50 focus:ring-violet-500/20 focus:border-violet-500/40 text-white placeholder-slate-400"
        />
      </div>
      <ScrollArea className="h-[140px]">
        <div className="space-y-1.5 pr-2">
          {filteredFiles.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-8 text-slate-400">
              <FileSearch className="h-8 w-8 mb-2 opacity-50" />
              <p className="text-sm">No matching files found</p>
            </div>
          ) : (
            filteredFiles.map((file, index) => (
              <div
                key={index}
                className="group flex items-center gap-3 p-2.5 rounded-lg hover:bg-slate-800/50 transition-all duration-200 border border-transparent hover:border-slate-700/50"
              >
                <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-violet-500/10 to-purple-600/10 group-hover:from-violet-500/20 group-hover:to-purple-600/20 flex items-center justify-center transition-all duration-200">
                  <File className="h-4 w-4 text-violet-400" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-slate-200 truncate font-medium">{file.name}</p>
                </div>
              </div>
            ))
          )}
        </div>
      </ScrollArea>
    </div>
  );
};
