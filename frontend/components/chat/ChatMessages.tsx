"use client";

import React, { useRef, useEffect } from "react";
import ReactMarkdown from 'react-markdown';

const MarkdownRenderer = ({ content }: { content: string }) => (
  <ReactMarkdown
    components={{
      p: ({ children }) => <p className="text-sm text-gray-200 leading-relaxed mb-2">{children}</p>,
      h1: ({ children }) => <h1 className="text-lg font-semibold text-gray-200 mb-3">{children}</h1>,
      h2: ({ children }) => <h2 className="text-base font-semibold text-gray-200 mb-2">{children}</h2>,
      h3: ({ children }) => <h3 className="text-sm font-semibold text-gray-200 mb-2">{children}</h3>,
      ul: ({ children }) => <ul className="list-disc ml-4 mb-3 text-gray-200">{children}</ul>,
      ol: ({ children }) => <ol className="list-decimal ml-4 mb-3 text-gray-200">{children}</ol>,
      li: ({ children }) => <li className="mb-1">{children}</li>,
      code: ({ children }) => (
        <pre className="bg-stone-950 rounded-lg p-3 my-2 font-mono text-sm text-gray-200 overflow-x-auto">
          <code>{children}</code>
        </pre>
      ),
      blockquote: ({ children }) => (
        <blockquote className="border-l-4 border-gray-700 pl-4 italic my-3 text-gray-300">{children}</blockquote>
      ),
      a: ({ children, href }) => (
        <a href={href} className="text-green-600 hover:underline" target="_blank" rel="noopener noreferrer">
          {children}
        </a>
      ),
    }}
  >
    {content}
  </ReactMarkdown>
);

// ChatMessages Component
export const ChatMessages = ({ messages }: { messages: string[] }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

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
                  <MarkdownRenderer content={text} />
                )}
              </div>
            </div>
          );
        })}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};
