"use client";
import { FileText } from "lucide-react";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

interface SourcesSectionProps {
  sources: string[];
}

export const SourcesSection = ({ sources }: SourcesSectionProps) => {
  return (
    <div className="p-4 h-1/2 border-t border-zinc-800 overflow-y-auto">
      <h2 className="text-sm font-semibold mb-4 text-gray-200 flex items-center space-x-2">
        <FileText className="h-4 w-4 text-green-600" />
        <span>Active Context Sources</span>
      </h2>

      {sources.length === 0 ? (
        <div className="text-sm text-gray-400 px-3 py-2">No active sources</div>
      ) : (
        <Accordion type="single" collapsible className="w-full space-y-1">
          {sources.map((source, index) => (
            <AccordionItem
              key={index}
              value={`source-${index}`}
              className="border-0 mb-1 overflow-hidden rounded-lg hover:bg-gray-800/50"
            >
              <AccordionTrigger className="rounded-lg px-3 py-2">
                <div className="flex items-center space-x-3">
                  <FileText className="h-4 w-4 text-green-600" />
                  <span className="text-sm text-gray-200">{source}</span>
                </div>
              </AccordionTrigger>

              <AccordionContent>
                <div style={{ height: "200px", overflowY: "auto" }}>
                  <iframe
                    src={`/api/get-pdfs?filename=${source}`}
                    style={{ width: "100%", height: "100%", border: "none" }}
                    title={source}
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
