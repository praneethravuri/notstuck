"use client"
import React, { useRef, useEffect } from "react";
import { Send} from "lucide-react";
import { Button } from "../../components/ui/button";

export const ChatInput = ({ onSendMessage }: { onSendMessage: (message: string) => void }) => {
  const [message, setMessage] = React.useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message);
      setMessage("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  }, [message]);

  return (
    <div className="fixed bottom-0 left-0 w-full bg-gradient-to-t from-stone-950 via-stone-950 to-transparent pt-20 pb-8">
      <div className="max-w-4xl mx-auto px-4">
        <form onSubmit={handleSubmit} className="relative">
          <div className="flex gap-2 items-end items-center">

            
            <div className="flex-1 relative">
              <textarea
                ref={textareaRef}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Message Oleve..."
                rows={1}
                className="w-full bg-stone-900 border border-gray-800 focus:border-green-600/50 focus:ring-0 rounded-xl
                      px-4 py-3 text-sm text-gray-200 focus:outline-none
                      placeholder-gray-400 resize-none max-h-[150px] overflow-hidden"
              />
            </div>

            <Button
              type="submit"
              size="icon"
              disabled={!message.trim()}
              className={`h-10 w-10 rounded-xl transition-all duration-200 p-6 ${
                message.trim()
                  ? 'bg-green-600 hover:bg-green-700 text-white'
                  : 'bg-stone-900 text-gray-500 cursor-not-allowed'
              }`}
            >
              <Send className="h-5 w-5" />
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};