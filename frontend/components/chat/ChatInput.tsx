"use client";
import React, { useRef, useEffect, useState } from "react";
import { Send, Paperclip, UploadCloud } from "lucide-react";
import { Button } from "../../components/ui/button";
import { Progress } from "../../components/ui/progress";

interface ChatInputProps {
  uploadHandler?: (files: FileList) => Promise<void>;
  isUploading?: boolean;
  onSendMessage: (message: string) => void;
}

export const ChatInput = ({ onSendMessage, uploadHandler, isUploading }: ChatInputProps) => {
  const [message, setMessage] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message);
      setMessage("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleFileUpload = async (files: FileList) => {
    if (uploadHandler) {
      await uploadHandler(files);
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
        {isUploading && (
          <div className="mb-4 p-4 bg-stone-900 rounded-xl border border-gray-800">
            <div className="flex items-center gap-3">
              <UploadCloud className="h-5 w-5 text-green-500 animate-pulse" />
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-200">Uploading Documents...</p>
                <Progress value={66} className="w-full mt-2" />
              </div>
            </div>
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="relative">
          <div className="flex gap-2 items-end">
            <input
              type="file"
              ref={fileInputRef}
              className="hidden"
              onChange={(e) => {
                if (e.target.files) {
                  handleFileUpload(e.target.files);
                }
              }}
              multiple
            />
            
            <Button
              type="button"
              size="icon"
              onClick={() => fileInputRef.current?.click()}
              className="h-10 w-10 rounded-xl bg-stone-900 hover:bg-stone-800 text-gray-400 p-6"
            >
              <Paperclip className="h-5 w-5" />
            </Button>
            
            <div className="flex-1 relative">
              <textarea
                ref={textareaRef}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Message or drop files here..."
                rows={1}
                className="w-full bg-stone-900 border border-gray-800 focus:border-green-600/50 focus:ring-0 rounded-xl
                        px-4 py-3 text-sm text-gray-200 focus:outline-none
                        placeholder-gray-400 resize-none max-h-[150px] overflow-hidden"
                onDragOver={(e: React.DragEvent<HTMLTextAreaElement>) => e.preventDefault()}
                onDrop={(e: React.DragEvent<HTMLTextAreaElement>) => {
                  e.preventDefault();
                  if (e.dataTransfer.files) {
                    handleFileUpload(e.dataTransfer.files);
                  }
                }}
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