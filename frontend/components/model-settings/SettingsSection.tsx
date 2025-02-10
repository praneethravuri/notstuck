"use client";
import { Wrench } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";

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
}

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
}: SettingsSectionProps) => {
  return (
    <div className="h-screen bg-stone-950 flex flex-col">
      <div className="flex items-center space-x-2 p-4">
        <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center ">
          <Wrench className="h-5 w-5 text-white" />
        </div>
        <span className="font-semibold text-gray-200">Fine Tuning</span>
      </div>
      <div className="border-t border-zinc-800 p-4">
          <div className="space-y-4">
            {/* Model Selection */}
            <div>
              <label className="text-sm text-gray-400 mb-2 block">Model</label>
              <Select defaultValue="gpt-4o">
                <SelectTrigger className="w-full bg-stone-900 focus:border-green-800 focus:ring-0">
                  <SelectValue placeholder="Select model" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="gpt-4o">GPT-4o</SelectItem>
                  <SelectItem value="gpt-4o-mini">GPT-4.0-Mini</SelectItem>
                  <SelectItem value="o1">o1</SelectItem>
                  <SelectItem value="o1-mini">o1-mini</SelectItem>
                  <SelectItem value="o3-mini">o3-mini</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Response Style */}
            <div>
              <label className="text-sm text-gray-400 mb-2 block">Response Style</label>
              <Select value={responseStyle} onValueChange={setResponseStyle}>
                <SelectTrigger className="w-full  bg-stone-900 focus:border-green-800 focus:ring-0">
                  <SelectValue placeholder="Select style" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="concise">Concise</SelectItem>
                  <SelectItem value="detailed">Detailed</SelectItem>
                  <SelectItem value="technical">Technical</SelectItem>
                  <SelectItem value="casual">Casual</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Temperature */}
            <div>
              <label className="text-sm text-gray-400 mb-2 block">Temperature</label>
              <Slider
                value={temperature}
                onValueChange={setTemperature}
                min={0}
                max={1}
                step={0.1}
                className="w-full  bg-green-600"
              />
              <span className="text-sm text-gray-400 mt-1 block">{temperature[0]}</span>
            </div>

            {/* Max Tokens */}
            <div>
              <label className="text-sm text-gray-400 mb-2 block">Max Tokens</label>
              <Slider
                value={maxTokens}
                onValueChange={setMaxTokens}
                min={500}
                max={4000}
                step={100}
                className="w-full bg-green-600"
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
                className="w-full bg-green-600"
              />
              <span className="text-sm text-gray-400 mt-1 block">{similarityThreshold[0]}</span>
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
                className="w-full bg-green-600"
              />
              <span className="text-sm text-gray-400 mt-1 block">{similarResults[0]}</span>
            </div>
          </div>
        </div>
    </div>
  );
};

export default SettingsSection;
