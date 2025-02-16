import React from "react";
import { FileText, BookOpen } from "lucide-react";
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "../../components/ui/accordion";
import { ScrollArea } from "../../components/ui/scroll-area";

interface SourceInfo {
  source_file: string;
  page_number?: number;
}

interface SourcesSectionProps {
  relevantChunks: string[];
  sources: SourceInfo[];
}

export const SourcesSection = ({ relevantChunks, sources }: SourcesSectionProps) => {
  return (
    <Accordion
      type="single"
      collapsible
      className="space-y-2"
    >
      <AccordionItem value="sources" className="border-none">
        <AccordionTrigger className="py-4 px-4 hover:no-underline hover:bg-stone-900/50">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-lg bg-green-500/10 flex items-center justify-center">
              <BookOpen className="h-4 w-4 text-green-500" />
            </div>
            <div>
              <h2 className="text-base font-medium text-gray-200">Active Sources</h2>
            </div>
          </div>
        </AccordionTrigger>
        <AccordionContent>
          <ScrollArea className="h-[calc(100vh/3-6rem)]">
            <div className="space-y-2 px-4">
              {relevantChunks.length === 0 ? (
                <div className="text-center py-8 space-y-3">
                  <FileText className="mx-auto h-12 w-12 text-gray-500/50" />
                  <div className="space-y-1">
                    <p className="text-sm font-medium text-gray-300">
                      No active sources
                    </p>
                    <p className="text-xs text-gray-500">
                      Sources will appear as you chat
                    </p>
                  </div>
                </div>
              ) : (
                <div className="space-y-2">
                  {relevantChunks.map((chunk, index) => {
                    const sourceInfo = sources[index] || {};
                    return (
                      <div key={index} className="bg-stone-900/50 rounded-lg overflow-hidden">
                        <Accordion type="single" collapsible>
                          <AccordionItem value={`item-${index}`} className="border-none">
                            <AccordionTrigger className="px-4 py-3 hover:no-underline hover:bg-stone-900/50">
                              <div className="flex items-center">
                                <FileText className="h-4 w-4 text-green-500" />
                                <span className="text-sm text-gray-200 ml-2">
                                  {sourceInfo.source_file || `Source ${index + 1}`}
                                  {sourceInfo.page_number !== undefined ? ` (Page ${sourceInfo.page_number + 1})` : ""}
                                </span>
                              </div>
                            </AccordionTrigger>
                            <AccordionContent>
                              <div className="px-4 py-3 text-sm text-gray-400">
                                {chunk}
                              </div>
                            </AccordionContent>
                          </AccordionItem>
                        </Accordion>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </ScrollArea>
        </AccordionContent>
      </AccordionItem>
    </Accordion>
  );
};