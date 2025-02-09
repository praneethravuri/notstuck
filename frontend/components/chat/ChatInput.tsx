"use client";
import React, { useRef, useEffect } from "react";
import { Send, PaperclipIcon, Smile, Mic } from "lucide-react";


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
    <div className="border-t border-gray-800 bg-gray-900/50 p-4">
      <form onSubmit={handleSubmit} className="flex items-end gap-2 max-w-4xl mx-auto">
        <button
          type="button"
          className="p-2 text-gray-400 hover:text-gray-300 transition-colors"
        >
          <PaperclipIcon className="h-5 w-5" />
        </button>
        
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
            rows={1}
            className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 pr-12 text-sm text-gray-200 
                     focus:outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-400
                     placeholder-gray-500 resize-none max-h-[150px]"
          />
          <button
            type="button"
            className="absolute right-3 bottom-3 text-gray-400 hover:text-gray-300 transition-colors"
          >
            <Smile className="h-5 w-5" />
          </button>
        </div>

        <button
          type="button"
          className="p-2 text-gray-400 hover:text-gray-300 transition-colors"
        >
          <Mic className="h-5 w-5" />
        </button>
        
        <button
          type="submit"
          disabled={!message.trim()}
          className={`p-3 rounded-xl transition-all duration-200 ${
            message.trim() 
              ? 'bg-blue-600 text-white hover:bg-blue-700' 
              : 'bg-gray-800 text-gray-500 cursor-not-allowed'
          }`}
        >
          <Send className="h-5 w-5" />
        </button>
      </form>
    </div>
  );
};