import { useState, useEffect } from 'react';
import { SettingsSection } from './SettingSection';
import { DocumentsSection } from './DocumentSection';
import { UploadSection } from './UploadSection';

const CustomSidebar = () => {
  const [similarity, setSimilarity] = useState([0.7]);
  const [files, setFiles] = useState<{ name: string }[]>([]);

  // CustomSidebar.tsx (client component)
  useEffect(() => {
    async function loadFiles() {
      try {
        const res = await fetch("http://localhost:8000/api/get-pdfs"); // match your FastAPI
        if (!res.ok) {
          throw new Error("Failed to fetch PDF list");
        }
        const data = await res.json(); // { files: ["doc1.pdf","doc2.pdf"] }
        const pdfFiles = data.files.map((filename: string) => ({ name: filename }));
        setFiles(pdfFiles);
      } catch (err) {
        console.error("Error fetching PDF list:", err);
      }
    }
    loadFiles();
  }, []);


  return (
    <div className="w-80 h-screen bg-gray-900/50 backdrop-blur-sm flex flex-col">
      <SettingsSection similarity={similarity} setSimilarity={setSimilarity} />
      <DocumentsSection files={files} />
      <UploadSection />
    </div>
  );
};

export default CustomSidebar;