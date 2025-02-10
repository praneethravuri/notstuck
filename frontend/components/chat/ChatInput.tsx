"use client";

import React, { useRef, useEffect } from "react";
import { Send } from "lucide-react";

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
    <div className="fixed bottom-0 left-0 w-full  p-4 ">
      <form onSubmit={handleSubmit} className="flex justify-center items-center max-w-4xl mx-auto">
        <div className="flex gap-2 items-end w-full max-w-[600px]">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Write a message here..."
            rows={1}
            className="flex-1 bg-stone-800 border border-green-800 focus:border-green-800 focus:ring-0 rounded-xl 
                     px-4 py-3 text-sm text-gray-200 focus:outline-none overflow-hidden
                     placeholder-gray-400 resize-none max-h-[150px]"
          />
          
          <button
            type="submit"
            disabled={!message.trim()}
            className={`p-3 rounded-xl transition-all duration-200 border border-green-800 ${
              message.trim()
                ? 'bg-green-600 text-white hover:bg-green-800'
                : 'bg-stone-800 text-gray-500 cursor-not-allowed'
            }`}
          >
            <Send className="h-5 w-5" />
          </button>
        </div>
      </form>
    </div>
  );
};
