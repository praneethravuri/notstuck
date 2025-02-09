"use client";

import { DocumentsSection } from "./DocumentSection";
import { SourcesSection } from "./SourcesSection";
import { UploadSection } from "./UploadSection";

interface PdfFile {
  name: string;
}

interface CustomSidebarProps {
  files: PdfFile[];
  sources: string[];
  // Optionally, the parent can pass a custom upload handler.
  uploadHandler?: (files: FileList) => Promise<void>;
}

const CustomSidebar = ({ files, sources, uploadHandler }: CustomSidebarProps) => {
  return (
    <div className="w-80 h-screen bg-gray-900/50 backdrop-blur-sm flex flex-col overflow-y-auto">
      {/* Documents Section */}
      <DocumentsSection files={files} />

      {/* Sources Section */}
      <SourcesSection sources={sources} />

      {/* Upload Section */}
      <UploadSection uploadHandler={uploadHandler} />
    </div>
  );
};

export default CustomSidebar;
