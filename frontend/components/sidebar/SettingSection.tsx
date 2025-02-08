import { Settings } from "lucide-react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";

interface SettingsSectionProps {
  similarity: number[];
  setSimilarity: (value: number[]) => void;
}

export const SettingsSection = ({ similarity, setSimilarity }: SettingsSectionProps) => {
  return (
    <div className="p-4 border-b border-gray-800">
      <div className="mb-6">
        <h2 className="text-sm font-semibold mb-4 text-gray-200 flex items-center space-x-2">
          <Settings className="h-4 w-4 text-blue-400" />
          <span>Settings</span>
        </h2>
        
        <div className="space-y-4">
          <div>
            <label className="text-sm text-gray-400 mb-2 block">Model</label>
            <Select defaultValue="gpt-4">
              <SelectTrigger className="w-full bg-gray-800 border-gray-700">
                <SelectValue placeholder="Select model" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="gpt-4">GPT-4</SelectItem>
                <SelectItem value="gpt-3.5">GPT-3.5</SelectItem>
                <SelectItem value="claude">Claude</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div>
            <label className="text-sm text-gray-400 mb-2 block">Similarity Threshold</label>
            <Slider
              value={similarity}
              onValueChange={setSimilarity}
              min={0}
              max={1}
              step={0.1}
              className="w-full"
            />
            <span className="text-sm text-gray-400 mt-1 block">{similarity[0]}</span>
          </div>
        </div>
      </div>
    </div>
  );
};