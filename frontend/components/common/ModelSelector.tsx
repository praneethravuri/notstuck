"use client";
import React, { useState, useEffect } from 'react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { Cpu, Loader2 } from "lucide-react";

interface ModelInfo {
  id: string;
  name: string;
  description?: string;
  context_length?: number;
  provider?: string;
}

interface ModelSelectorProps {
  modelName: string;
  setModelName: (value: string) => void;
}

export const ModelSelector = ({ modelName, setModelName }: ModelSelectorProps) => {
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        setIsLoading(true);
        const response = await fetch('/api/models');

        if (!response.ok) {
          throw new Error('Failed to fetch models');
        }

        const data = await response.json();

        if (data.models && Array.isArray(data.models)) {
          setModels(data.models);

          // Set default model if current selection is not in the list
          if (!modelName || !data.models.find((m: ModelInfo) => m.id === modelName)) {
            setModelName(data.models[0]?.id || 'openai/gpt-4o');
          }
        }
      } catch (err) {
        console.error('Error fetching models:', err);
        setError('Failed to load models');

        // Fallback to default models
        const fallbackModels = [
          { id: "openai/gpt-4o", name: "GPT-4o", provider: "openai" },
          { id: "openai/gpt-4o-mini", name: "GPT-4o Mini", provider: "openai" },
        ];
        setModels(fallbackModels);
        if (!modelName) {
          setModelName(fallbackModels[0].id);
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchModels();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center gap-2">
        <Loader2 className="h-4 w-4 text-violet-400 animate-spin" />
        <span className="text-sm text-slate-400">Loading models...</span>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2">
      <Cpu className="h-4 w-4 text-violet-400" />
      <Select value={modelName} onValueChange={setModelName}>
        <SelectTrigger
          className="w-56 border border-slate-800/50 bg-slate-900/50 hover:bg-slate-800/50 focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500/50
          transition-all duration-200 rounded-lg px-3 py-2 flex items-center justify-between backdrop-blur-sm"
        >
          <SelectValue
            placeholder="Select model"
            className="text-sm font-medium text-white"
          />
        </SelectTrigger>
        <SelectContent className="bg-slate-900 border border-slate-800 rounded-lg shadow-xl backdrop-blur-sm max-h-96 overflow-y-auto">
          {models.map((model) => (
            <SelectItem
              key={model.id}
              value={model.id}
              className="py-2.5 px-3 focus:bg-violet-500/10 hover:bg-slate-800
              transition-all duration-200 cursor-pointer text-sm text-white
              data-[state=checked]:bg-violet-500/10 data-[state=checked]:text-violet-400"
            >
              <div className="flex flex-col">
                <span className="font-medium">{model.name}</span>
                {model.provider && (
                  <span className="text-xs text-slate-500">{model.provider}</span>
                )}
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      {error && (
        <span className="text-xs text-red-400" title={error}>⚠</span>
      )}
    </div>
  );
};

export default ModelSelector;
