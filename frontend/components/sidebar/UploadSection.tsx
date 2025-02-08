import { Upload } from "lucide-react";

export const UploadSection = () => {
  return (
    <div className="p-4 border-t border-gray-800">
      <h2 className="text-sm font-semibold mb-4 text-gray-200 flex items-center space-x-2">
        <Upload className="h-4 w-4 text-blue-400" />
        <span>Upload Documents</span>
      </h2>
      <div 
        className="border-2 border-dashed border-gray-700 rounded-lg p-6 text-center hover:border-blue-400 transition-colors duration-200 cursor-pointer"
        onDragOver={(e) => e.preventDefault()}
      >
        <input
          id="file-upload"
          type="file"
          className="hidden"
          multiple
          onChange={(e) => {
            console.log(e.target.files);
          }}
        />
        <Upload className="h-8 w-8 text-gray-400 mx-auto mb-2" />
        <p className="text-sm text-gray-400">
          Drag and drop files here or <span className="text-blue-400">browse</span>
        </p>
        <p className="text-xs text-gray-500 mt-1">
          Supports PDF, TXT, DOC, DOCX
        </p>
      </div>
    </div>
  );
};