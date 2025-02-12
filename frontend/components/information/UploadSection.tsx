"use client";
import { Upload, UploadCloud } from "lucide-react";
import axios from "axios";
import { Card } from "../ui/card";
import { Progress } from "../ui/progress";


interface UploadSectionProps {
  // Optional custom upload handler.
  uploadHandler?: (files: FileList) => Promise<void>;
  isUploading?: boolean;
}

export const UploadSection = ({ uploadHandler, isUploading }: UploadSectionProps) => {
  const handleFileUpload = async (files: FileList) => {
    if (uploadHandler) {
      await uploadHandler(files);
      return;
    }
    try {
      const formData = new FormData();
      Array.from(files).forEach((file) => {
        formData.append("files", file);
      });
      const response = await axios.post("/api/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      console.log("Upload successful:", response.data);
    } catch (error) {
      console.error("Upload failed:", error);
    }
  };

  return (
    <Card className="border-none p-4 space-y-4">
      <div className="flex items-center gap-3">
        <div className="h-8 w-8 rounded-lg bg-green-500/10 flex items-center justify-center">
          <Upload className="h-4 w-4 text-green-500" />
        </div>
        <h2 className="text-base font-medium text-gray-200">Upload Documents</h2>
      </div>

      <div
        className={`
          relative border-2 border-dashed border-gray-700 rounded-lg
          ${isUploading ? 'bg-stone-800/50' : 'hover:bg-green-600/30'}
          transition-colors duration-200
        `}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          if (e.dataTransfer.files) {
            handleFileUpload(e.dataTransfer.files);
          }
        }}
      >
        <input
          type="file"
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          onChange={(e) => {
            if (e.target.files) {
              handleFileUpload(e.target.files);
            }
          }}
          multiple
        />

        {isUploading ? (
          <div className="flex flex-col items-center justify-center py-8">
            <div className="relative">
              <UploadCloud className="h-10 w-10 text-green-500 animate-pulse" />
              <Progress value={66} className="w-24 mt-4" />
            </div>
            <div className="mt-4 text-center">
              <p className="text-sm font-medium text-gray-200">Uploading Documents...</p>
              <p className="text-xs text-gray-400 mt-1">Your knowledge base is expanding</p>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-8">
            <UploadCloud className="h-10 w-10 text-gray-400 mb-2" />
            <p className="text-sm text-gray-300">Drop files here or click to upload</p>
            <p className="text-xs text-gray-400 mt-1">PDF, TXT, DOC files supported</p>
          </div>
        )}
      </div>
    </Card>
  );
};
