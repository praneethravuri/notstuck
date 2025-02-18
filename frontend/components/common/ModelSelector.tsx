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
    <div className="p-2 flex items-center">
      <Select value={modelName} onValueChange={setModelName}>
        <SelectTrigger className="w-50 border-none focus:bg-stone-950 ring-0 focus:border-none focus:ring-0">
          <SelectValue placeholder="Select model" />
        </SelectTrigger>
        <SelectContent className="bg-stone-950">
          {models.map((model) => (
            <SelectItem
              key={model.modelName}
              value={model.modelName}
              className="py-3 focus:bg-green-500/10"
            >
              {model.displayName}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};