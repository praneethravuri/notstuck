import React from 'react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";

interface ModelSelectorProps {
  modelName: string;
  setModelName: (value: string) => void;
}

export const ModelSelector = ({ modelName, setModelName }: ModelSelectorProps) => {
  const models = [
    { modelName: "gpt-4o", displayName: "GPT-4o" },
    { modelName: "gpt-4o-mini", displayName: "GPT-4.0-Mini" },
  ];

  return (
    <div className="p-4 flex items-center">
      <Select value={modelName} onValueChange={setModelName}>
        <SelectTrigger 
          className="w-40 border-none focus:bg-stone-950 ring-0 focus:border-none focus:ring-0
          hover:bg-stone-800 transition-colors duration-200 rounded-lg px-4 py-2 flex items-center justify-between"
        >
          <SelectValue 
            placeholder="Select model" 
            className="text-lg font-medium"
          />
        </SelectTrigger>
        <SelectContent className="bg-stone-950 border border-stone-800 rounded-lg shadow-lg">
          {models.map((model) => (
            <SelectItem
              key={model.modelName}
              value={model.modelName}
              className="py-3 px-4 focus:bg-green-500/10 hover:bg-stone-800 
              transition-colors duration-200 cursor-pointer text-lg font-medium"
            >
              {model.displayName}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};

export default ModelSelector;