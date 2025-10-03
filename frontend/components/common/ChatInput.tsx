"use client";
import React, { useRef, useEffect, useState } from "react";
import { Send, Paperclip, UploadCloud } from "lucide-react";
import { Button } from "../ui/button";
import { Progress } from "../ui/progress";

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
    <div className="w-full">
      {isUploading && (
        <div className="mb-4 p-4 bg-slate-900/50 rounded-xl border border-slate-800/50 backdrop-blur-sm">
          <div className="flex items-center gap-3">
            <UploadCloud className="h-5 w-5 text-violet-400 animate-pulse" />
            <div className="flex-1">
              <p className="text-sm font-semibold text-white mb-2">Uploading Documents...</p>
              <Progress value={66} className="w-full h-2 bg-slate-800" />
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
            className="h-12 w-12 rounded-xl bg-slate-900/50 hover:bg-slate-800 border border-slate-800/50 text-slate-400 hover:text-violet-400 transition-all duration-200 hover:border-violet-500/30"
          >
            <Paperclip className="h-5 w-5" />
          </Button>

          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question about your documents..."
              rows={1}
              className="w-full bg-slate-900/50 border border-slate-800/50 focus:border-violet-500/50 focus:ring-2 focus:ring-violet-500/20 rounded-xl
                      px-4 py-3 text-sm text-white focus:outline-none
                      placeholder-slate-500 resize-none max-h-[150px] overflow-hidden backdrop-blur-sm transition-all duration-200"
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
            className={`h-12 w-12 rounded-xl transition-all duration-200 ${message.trim()
              ? 'bg-gradient-to-br from-violet-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 text-white shadow-lg shadow-violet-900/30'
              : 'bg-slate-900/50 text-slate-500 cursor-not-allowed border border-slate-800/50'
              }`}
          >
            <Send className="h-5 w-5" />
          </Button>
        </div>
      </form>
    </div>
  );
};
