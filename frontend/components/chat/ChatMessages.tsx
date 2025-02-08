"use client";
import React from "react";

interface ChatMessagesProps {
  messages: string[];
}

export const ChatMessages = ({ messages }: ChatMessagesProps) => {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`p-3 rounded-lg max-w-[80%] ${
            message.startsWith("You:")
              ? "bg-blue-600/10 text-blue-200 ml-auto"
              : "bg-gray-800/50 text-gray-200"
          }`}
        >
          <p className="text-sm">{message}</p>
        </div>
      ))}
    </div>
  );
};