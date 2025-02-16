import React from 'react';
import { Settings2, Zap, Binary, Clock, Share2, BrainCircuit } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../../components/ui/select";
import { Slider } from "../../components/ui/slider";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../../components/ui/accordion";
import { Card } from "../../components/ui/card";

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
  { modelName: "gpt-4o", displayName: "GPT-4o", description: "Most capable model, best for complex tasks" },
  { modelName: "gpt-4o-mini", displayName: "GPT-4.0-Mini", description: "Faster, optimized for simpler tasks" },
];

const responseStyles = [
  { style: "concise", displayName: "Concise", icon: Zap },
  { style: "detailed", displayName: "Detailed", icon: Clock },
  { style: "technical", displayName: "Technical", icon: Binary },
  { style: "casual", displayName: "Casual", icon: Share2 },
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
    <div className="bg-stone-950 p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="h-10 w-10 rounded-lg bg-green-500/10 flex items-center justify-center">
          <BrainCircuit className="h-5 w-5 text-green-500" />
        </div>
        <div>
          <h2 className="text-lg font-semibold text-gray-200">Model Settings</h2>
          <p className="text-sm text-gray-400">Configure your AI assistant</p>
        </div>
      </div>

      {/* Model Selection Card */}
      <Card className="bg-stone-900/50 border-gray-800 p-4 space-y-4">
        <label className="text-sm font-medium text-gray-300">Model</label>
        <Select value={modelName} onValueChange={setModelName}>
          <SelectTrigger className="w-full bg-stone-800 border-gray-700 focus:ring-green-500/20 focus:border-green-500/40">
            <SelectValue placeholder="Select model" />
          </SelectTrigger>
          <SelectContent>
            {models.map((model) => (
              <SelectItem 
                key={model.modelName} 
                value={model.modelName}
                className="py-3"
              >
                <div className="space-y-1">
                  <div className="font-medium">{model.displayName}</div>
                  <div className="text-xs text-gray-400">{model.description}</div>
                </div>
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </Card>

      {/* Response Style Grid */}
      <div className="space-y-2">
        <label className="text-sm font-medium text-gray-300">Response Style</label>
        <div className="grid grid-cols-2 gap-3">
          {responseStyles.map(({ style, displayName, icon: Icon }) => (
            <button
              key={style}
              onClick={() => setResponseStyle(style)}
              className={`p-3 rounded-lg border transition-all duration-200 flex items-center gap-2
                ${responseStyle === style 
                  ? 'border-green-500/50 bg-green-500/10 text-green-500' 
                  : 'border-gray-800 bg-stone-900/50 text-gray-400 hover:bg-stone-800'
                }`}
            >
              <Icon className="h-4 w-4" />
              <span className="text-sm font-medium">{displayName}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Advanced Settings */}
      <Accordion type="single" collapsible className="w-full">
        <AccordionItem value="advanced-settings" className="border-gray-800">
          <AccordionTrigger className="text-gray-200 hover:text-gray-100">
            <div className="flex items-center gap-2">
              <Settings2 className="h-4 w-4 text-green-500" />
              <span className="text-sm font-medium">Advanced Settings</span>
            </div>
          </AccordionTrigger>
          <AccordionContent>
            <div className="space-y-6 pt-4">
              {/* Sliders with improved visual feedback */}
              {[
                {
                  label: "Temperature",
                  value: temperature,
                  setValue: setTemperature,
                  min: 0,
                  max: 1,
                  step: 0.1,
                  format: (v: number) => v.toFixed(1),
                },
                {
                  label: "Max Tokens",
                  value: maxTokens,
                  setValue: setMaxTokens,
                  min: 5000,
                  max: 20000,
                  step: 1000,
                  format: (v: number) => v.toLocaleString(),
                },
                {
                  label: "Similarity Threshold",
                  value: similarityThreshold,
                  setValue: setSimilarityThreshold,
                  min: 0,
                  max: 1,
                  step: 0.1,
                  format: (v: number) => `${(v * 100).toFixed(0)}%`,
                },
                {
                  label: "Similar Results",
                  value: similarResults,
                  setValue: setSimilarResults,
                  min: 5,
                  max: 10,
                  step: 1,
                  format: (v: number) => v.toString(),
                },
              ].map((setting) => (
                <div key={setting.label} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <label className="text-sm font-medium text-gray-300">
                      {setting.label}
                    </label>
                    <span className="text-sm text-green-500">
                      {setting.format(setting.value[0])}
                    </span>
                  </div>
                  <Slider
                    value={setting.value}
                    onValueChange={setting.setValue}
                    min={setting.min}
                    max={setting.max}
                    step={setting.step}
                    className="w-full"
                  />
                </div>
              ))}
            </div>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>
  );
};

export default SettingsSection;