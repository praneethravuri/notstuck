import React from 'react';
import { Settings2 } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { Slider } from "../ui/slider";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../ui/accordion";

interface SettingsSectionProps {
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
  modelName: string;
  setModelName: (value: string) => void;
}

const models = [
  { modelName: "gpt-4o", displayName: "GPT-4o" },
  { modelName: "gpt-4o-mini", displayName: "GPT-4.0-Mini" },
];

const responseStyles = [
  { style: "concise", displayName: "Concise" },
  { style: "detailed", displayName: "Detailed" },
  { style: "technical", displayName: "Technical" },
  { style: "casual", displayName: "Casual" },
];

export const SettingsSection = ({
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
  modelName,
  setModelName,
}: SettingsSectionProps) => {
  return (
    <div className=" bg-stone-950 flex flex-col">
      <div className="p-4">
        <div className="space-y-4">
          {/* Primary Settings */}
          <div>
            <label className="text-sm text-gray-400 mb-2 block">Model</label>
            <Select value={modelName} onValueChange={setModelName}>
              <SelectTrigger className="w-full bg-stone-900 focus:border-green-800 focus:ring-0">
                <SelectValue placeholder="Select model" />
              </SelectTrigger>
              <SelectContent>
                {models.map((model) => (
                  <SelectItem key={model.modelName} value={model.modelName}>
                    {model.displayName}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div>
            <label className="text-sm text-gray-400 mb-2 block">Response Style</label>
            <Select value={responseStyle} onValueChange={setResponseStyle}>
              <SelectTrigger className="w-full bg-stone-900 focus:border-green-800 focus:ring-0">
                <SelectValue placeholder="Select style" />
              </SelectTrigger>
              <SelectContent>
                {responseStyles.map((style) => (
                  <SelectItem key={style.style} value={style.style}>
                    {style.displayName}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Advanced Settings Accordion */}
          <Accordion type="single" collapsible className="w-full">
            <AccordionItem value="advanced-settings" className="border-zinc-800">
              <AccordionTrigger className="text-gray-200 hover:text-gray-100">
                <div className="flex items-center space-x-2">
                  <Settings2 className="h-4 w-4 text-green-600" />
                  <span>Advanced Settings</span>
                </div>
              </AccordionTrigger>
              <AccordionContent>
                <div className="space-y-6 pt-4">
                  {/* Temperature */}
                  <div>
                    <label className="text-sm text-gray-400 mb-2 block">Temperature</label>
                    <Slider
                      value={temperature}
                      onValueChange={setTemperature}
                      min={0}
                      max={1}
                      step={0.1}
                      className="w-full"
                    />
                    <span className="text-sm text-gray-400 mt-1 block">{temperature[0]}</span>
                  </div>

                  {/* Max Tokens */}
                  <div>
                    <label className="text-sm text-gray-400 mb-2 block">Max Tokens</label>
                    <Slider
                      value={maxTokens}
                      onValueChange={setMaxTokens}
                      min={5000}
                      max={20000}
                      step={1000}
                      className="w-full"
                    />
                    <span className="text-sm text-gray-400 mt-1 block">{maxTokens[0]}</span>
                  </div>

                  {/* Similarity Threshold */}
                  <div>
                    <label className="text-sm text-gray-400 mb-2 block">Similarity Threshold</label>
                    <Slider
                      value={similarityThreshold}
                      onValueChange={setSimilarityThreshold}
                      min={0}
                      max={1}
                      step={0.1}
                      className="w-full"
                    />
                    <span className="text-sm text-gray-400 mt-1 block">{similarityThreshold[0] * 100}%</span>
                  </div>

                  {/* Similar Results */}
                  <div>
                    <label className="text-sm text-gray-400 mb-2 block">Similar Results</label>
                    <Slider
                      value={similarResults}
                      onValueChange={setSimilarResults}
                      min={5}
                      max={15}
                      step={1}
                      className="w-full"
                    />
                    <span className="text-sm text-gray-400 mt-1 block">{similarResults[0]}</span>
                  </div>
                </div>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </div>
    </div>
  );
};

export default SettingsSection;