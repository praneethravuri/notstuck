"use client";

import React, { useRef, useEffect } from "react";
import ReactMarkdown from 'react-markdown';

// ChatMessages Component
export const ChatMessages = ({ messages, isLoading }: { messages: string[], isLoading: boolean }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]); // Also trigger scroll when loading state changes

  return (
    <div className="flex-1 overflow-y-auto p-4 pb-24"> {/* Ensures proper scrolling and input space */}
      <div className="flex flex-col space-y-6">
        {messages.map((message, index) => {
          const isUser = message.startsWith("You:");
          const text = message.replace(/^(You:|AI:)\s*/, '');
          
          return (
            <div
              key={index}
              className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`
                  max-w-[85%] rounded-xl p-4
                  ${isUser
                    ? 'bg-green-600 text-white'
                    : 'bg-stone-950 text-gray-200'
                  }
                `}
              >
                {isUser ? (
                  <p className="text-sm leading-relaxed whitespace-pre-wrap">{text}</p>
                ) : (
                  <ReactMarkdown>{text}</ReactMarkdown>
                )}
              </div>
            </div>
          );
        })}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-[85%] rounded-xl p-4 bg-stone-950 text-gray-200">
              <p className="text-sm leading-relaxed">AI is typing...</p>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};