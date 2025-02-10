"use client";
import { Upload } from "lucide-react";
import axios from "axios";

interface UploadSectionProps {
  // Optional custom upload handler.
  uploadHandler?: (files: FileList) => Promise<void>;
}

export const UploadSection = ({ uploadHandler }: UploadSectionProps) => {
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
    <div className="p-4 border-t border-zinc-800">
      <h2 className="text-sm font-semibold mb-4 text-gray-200 flex items-center space-x-2">
        <Upload className="h-4 w-4 text-green-600" />
        <span>Upload Documents</span>
      </h2>

      <div
        className="border-2 border-dashed border-gray-700 rounded-lg p-6 text-center hover:border-green-600 transition-colors duration-200 cursor-pointer"
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          if (e.dataTransfer.files) {
            handleFileUpload(e.dataTransfer.files);
          }
        }}
      >
        <input
          id="file-upload"
          type="file"
          className="hidden"
          multiple
          onChange={(e) => {
            if (e.target.files) {
              handleFileUpload(e.target.files);
            }
          }}
        />
        <label htmlFor="file-upload" className="cursor-pointer">
          <Upload className="h-8 w-8 text-gray-400 mx-auto mb-2" />
          <p className="text-sm text-gray-400">
            Drag and drop files here or <span className="text-green-600">browse</span>
          </p>
        </label>
      </div>
    </div>
  );
};
