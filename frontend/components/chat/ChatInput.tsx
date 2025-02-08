import { useState } from "react";
import { Button } from "@/components/ui/button";
import { SendIcon } from "lucide-react";
import { Textarea } from "@/components/ui/textarea";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
}

export default function ChatInput({ onSendMessage }: ChatInputProps) {
  const [inputValue, setInputValue] = useState("");

  const handleSend = () => {
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="p-4">
      <div className="flex items-center gap-2 max-w-4xl mx-auto bg-gray-800 rounded-lg p-2">
        <Textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Message NotStuck"
          className="min-h-[100px] bg-transparent border-0 focus-visible:ring-0 focus-visible:ring-offset-0 text-gray-200 placeholder:text-gray-400 resize-none flex-1"
        />
        <Button
          onClick={handleSend}
          className="bg-blue-500 hover:bg-blue-600 text-white transition-colors h-10 px-4 self-center"
        >
          <SendIcon className="h-4 w-4 mr-2" />
          Send
        </Button>
      </div>
    </div>
  );
}