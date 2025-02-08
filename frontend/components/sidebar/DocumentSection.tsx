"use client";
import { Database, FolderIcon } from "lucide-react";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

interface PdfFile {
  name: string; // e.g. "doc1.pdf"
}

interface DocumentsSectionProps {
  files: PdfFile[];
}

export const DocumentsSection = ({ files }: DocumentsSectionProps) => {
  return (
    <div className="p-4 border-b border-gray-800 flex-1 overflow-y-auto">
      <h2 className="text-sm font-semibold mb-4 text-gray-200 flex items-center space-x-2">
        <Database className="h-4 w-4 text-blue-400" />
        <span>Documents</span>
      </h2>
      <Accordion type="single" collapsible className="w-full space-y-1">
        {files.map((file, index) => (
          <AccordionItem
            key={index}
            value={`pdf-${index}`}
            className="border-0 mb-1 overflow-hidden rounded-lg hover:bg-gray-800/50"
          >
            <AccordionTrigger className="rounded-lg px-3 py-2">
              <div className="flex items-center space-x-3">
                <FolderIcon className="h-4 w-4 text-blue-400" />
                <span className="text-sm text-gray-200">{file.name}</span>
              </div>
            </AccordionTrigger>

            <AccordionContent>
              <div style={{ height: "500px", overflowY: "auto" }}>
                {/* 
                  Render a PDF in an iframe. 
                  The browser will natively handle display if it supports PDF embedding.
                */}
                <iframe
                  src={`http://localhost:8000/api/get-pdfs?filename=${file.name}`}
                  style={{ width: "100%", height: "100%", border: "none" }}
                />
              </div>
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </div>
  );
};
