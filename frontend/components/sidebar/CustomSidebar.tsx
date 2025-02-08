import { useState } from 'react';
import { SettingsSection } from './SettingSection';
import { DocumentsSection } from './DocumentSection';
import { UploadSection } from './UploadSection';

const CustomSidebar = () => {
  const [similarity, setSimilarity] = useState([0.7]);
  
  const files = [
    { name: "Document 1", content: ["Content 1", "Content 2"] },
    { name: "Document 2", content: ["Content 3", "Content 4"] },
    { name: "Document 3", content: ["Content 5", "Content 6"] },
  ];

  return (
    <div className="w-80 h-screen bg-gray-900/50 backdrop-blur-sm flex flex-col">
      <SettingsSection similarity={similarity} setSimilarity={setSimilarity} />
      <DocumentsSection files={files} />
      <UploadSection />
    </div>
  );
};

export default CustomSidebar;