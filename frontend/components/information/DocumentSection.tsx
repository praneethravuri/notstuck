"use client";

import { useState } from "react";
import { Database, FolderIcon, Search } from "lucide-react";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Input } from "@/components/ui/input";

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
    <div className="p-4 border-t border-zinc-800 h-1/2 overflow-y-auto">
      <h2 className="text-sm font-semibold mb-4 text-gray-200 flex items-center space-x-2">
        <Database className="h-4 w-4 text-green-600" />
        <span>Documents</span>
      </h2>

      {/* Search Bar */}
      <div className="mb-4">
        <div className="relative">
          <Search className="h-4 w-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <Input
            type="text"
            placeholder="Search documents..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 bg-stone-900 focus:border-green-800 focus:ring-0"
          />
        </div>
      </div>

      {/* Files List */}
      {filteredFiles.length === 0 ? (
        <div className="text-sm text-gray-400 px-3 py-2">No matching files found</div>
      ) : (
        <Accordion type="single" collapsible className="w-full overflow-y-auto space-y-1">
          {filteredFiles.map((file, index) => (
            <AccordionItem
              key={index}
              value={`pdf-${index}`}
              className="border-0 mb-1 overflow-hidden rounded-lg "
            >
              <AccordionTrigger className="rounded-lg px-1 py-2">
                <div className="flex items-center space-x-1">
                  <FolderIcon className="h-4 w-4 text-green-600" />
                  <span className="text-sm text-gray-200">{file.name}</span>
                </div>
              </AccordionTrigger>

              <AccordionContent>
                <div style={{ height: "500px", overflowY: "auto" }}>
                  <iframe
                    src={`http://localhost:8000/api/get-pdfs?filename=${file.name}`}
                    style={{ width: "100%", height: "100%", border: "none" }}
                    title={file.name}
                  />
                </div>
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      )}
    </div>
  );
};
