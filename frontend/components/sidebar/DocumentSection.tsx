import { Database, ChevronRight, FolderIcon, FileIcon } from "lucide-react";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

interface File {
  name: string;
  content: string[];
}

interface DocumentsSectionProps {
  files: File[];
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
            value={`item-${index}`} 
            className="border-0 mb-1 overflow-hidden rounded-lg transition-all duration-200 hover:bg-gray-800/50"
          >
            <AccordionTrigger className="hover:no-underline rounded-lg px-3 py-2 transition-all duration-200">
              <div className="flex items-center space-x-3 w-full">
                <div className="flex items-center space-x-3 flex-1">
                  <FolderIcon className="h-4 w-4 text-blue-400" />
                  <span className="text-sm text-gray-200">{file.name}</span>
                </div>
                <ChevronRight className="h-4 w-4 text-gray-400 transition-transform duration-200" />
              </div>
            </AccordionTrigger>
            <AccordionContent>
              <ul className="space-y-1 pl-8 py-2">
                {file.content.map((item, itemIndex) => (
                  <li
                    key={itemIndex}
                    className="group flex items-center space-x-3 px-2 py-1.5 rounded-md transition-all duration-200 hover:bg-gray-700/50"
                  >
                    <FileIcon className="h-4 w-4 text-gray-400 group-hover:text-blue-400 transition-colors duration-200" />
                    <span className="text-sm text-gray-400 group-hover:text-gray-200 transition-colors duration-200">
                      {item}
                    </span>
                  </li>
                ))}
              </ul>
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </div>
  );
};