"use client";
import { SettingsSection } from './SettingSection';
import { UploadSection } from './UploadSection';

interface LeftSidebarProps {
  similarityThreshold: number[];
  setSimilarityThreshold: (value: number[]) => void;
  similarResults: number[];
  setSimilarResults: (value: number[]) => void;
  temperature: number[];
  setTemperature: (value: number[]) => void;
  maxTokens: number[];
  setMaxTokens: (value: number[]) => void;
  responseStyle: string;
  setResponseStyle: (value: string) => void;
}

const LeftSidebar = ({
  similarityThreshold,
  setSimilarityThreshold,
  similarResults,
  setSimilarResults,
  temperature,
  setTemperature,
  maxTokens,
  setMaxTokens,
  responseStyle,
  setResponseStyle,
}: LeftSidebarProps) => {
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