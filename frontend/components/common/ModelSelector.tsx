import React from 'react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { Cpu } from "lucide-react";

interface ModelSelectorProps {
  modelName: string;
  setModelName: (value: string) => void;
}

export const ModelSelector = ({ modelName, setModelName }: ModelSelectorProps) => {
  const models = [
    { modelName: "gpt-4o", displayName: "GPT-4o" },
    { modelName: "gpt-4o-mini", displayName: "GPT-4o Mini" },
  ];

  return (
    <div className="flex items-center gap-2">
      <Cpu className="h-4 w-4 text-violet-400" />
      <Select value={modelName} onValueChange={setModelName}>
        <SelectTrigger
          className="w-40 border border-slate-800/50 bg-slate-900/50 hover:bg-slate-800/50 focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500/50
          transition-all duration-200 rounded-lg px-3 py-2 flex items-center justify-between backdrop-blur-sm"
        >
          <SelectValue
            placeholder="Select model"
            className="text-sm font-medium text-white"
          />
        </SelectTrigger>
        <SelectContent className="bg-slate-900 border border-slate-800 rounded-lg shadow-xl backdrop-blur-sm">
          {models.map((model) => (
            <SelectItem
              key={model.modelName}
              value={model.modelName}
              className="py-2.5 px-3 focus:bg-violet-500/10 hover:bg-slate-800
              transition-all duration-200 cursor-pointer text-sm font-medium text-white
              data-[state=checked]:bg-violet-500/10 data-[state=checked]:text-violet-400"
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
