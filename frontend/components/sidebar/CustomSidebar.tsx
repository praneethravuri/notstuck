// CustomSidebar.tsx
"use client";

import { DocumentsSection } from "./DocumentSection";
import { SourcesSection } from "./SourcesSection";
import { UploadSection } from "./UploadSection";
import { MessageSquare } from "lucide-react";

interface PdfFile {
  name: string;
}

interface CustomSidebarProps {
  files: PdfFile[];
  sources: string[]; // if needed elsewhere (e.g., for file names)
  uploadHandler?: (files: FileList) => Promise<void>;
  relevantChunks: string[]; // NEW prop for the chunks from the backend
}

const CustomSidebar = ({ files, uploadHandler, relevantChunks }: CustomSidebarProps) => {
  return (
    <div className="h-screen bg-stone-950 flex flex-col">
      {/* Logo Section */}
      <div className="p-4 flex items-center space-x-2">
        <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
          <MessageSquare className="h-5 w-5 text-white" />
        </div>
        <span className="font-semibold text-gray-200">NotStuck</span>
      </div>

      <div className="h-screen flex flex-col justify-between overflow-y-auto">
        {/* Documents Section */}
        <DocumentsSection files={files} />

        {/* Sources Section – pass the relevant chunks to be displayed as cards */}
        <SourcesSection relevantChunks={relevantChunks} />

        {/* Upload Section */}
        <UploadSection uploadHandler={uploadHandler} />
      </div>
    </div>
  );
};

export default CustomSidebar;
