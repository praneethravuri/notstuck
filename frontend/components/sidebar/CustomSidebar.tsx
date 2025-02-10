"use client";
import { useState } from "react";
import { DocumentsSection } from "./DocumentSection";
import { SourcesSection } from "./SourcesSection";
import { UploadSection } from "./UploadSection";

import { MessageSquare, Home, Database, Sliders, BookOpen, Settings, Users, CreditCard, FileText } from "lucide-react";

interface PdfFile {
  name: string;
}

interface CustomSidebarProps {
  files: PdfFile[];
  sources: string[];
  uploadHandler?: (files: FileList) => Promise<void>;
}

const CustomSidebar = ({ files, sources, uploadHandler }: CustomSidebarProps) => {
  return (
    <div className="h-screen bg-stone-950 flex flex-col">
      {/* Logo Section */}
      <div className="p-4 flex items-center space-x-2">
        <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
          <MessageSquare className="h-5 w-5 text-white" />
        </div>
        <span className="font-semibold text-gray-200">NotStuck</span>
      </div>

      <div className="h-screen  flex flex-col justify-between overflow-y-auto">
        {/* Documents Section */}
        <DocumentsSection files={files} />

        {/* Sources Section */}
        <SourcesSection sources={sources} />

        {/* Upload Section */}
        <UploadSection uploadHandler={uploadHandler} />
      </div>
    </div>
  );
};


export default CustomSidebar;