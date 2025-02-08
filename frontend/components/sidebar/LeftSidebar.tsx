"use client";
import { useState} from 'react';
import { SettingsSection } from './SettingSection';
import { UploadSection } from './UploadSection';

const LeftSidebar = () => {
  // State for settings
  const [similarityThreshold, setSimilarityThreshold] = useState([0.7]);
  const [similarResults, setSimilarResults] = useState([7]);
  const [temperature, setTemperature] = useState([0.5]);
  const [maxTokens, setMaxTokens] = useState([2000]);
  const [responseStyle, setResponseStyle] = useState("detailed");

  return (
    <div className="w-80 h-screen bg-gray-900/50 backdrop-blur-sm flex flex-col">
      {/* Settings Section */}
      <SettingsSection 
        similarityThreshold={similarityThreshold}
        setSimilarityThreshold={setSimilarityThreshold}
        similarResults={similarResults}
        setSimilarResults={setSimilarResults}
        temperature={temperature}
        setTemperature={setTemperature}
        maxTokens={maxTokens}
        setMaxTokens={setMaxTokens}
        responseStyle={responseStyle}
        setResponseStyle={setResponseStyle}
      />
      {/* Upload Section */}
      <UploadSection />
    </div>
  );
};

export default LeftSidebar;