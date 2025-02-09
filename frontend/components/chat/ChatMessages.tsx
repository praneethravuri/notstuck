"use client";

import React, { useRef, useEffect } from "react";
import ReactMarkdown from 'react-markdown';

// MarkdownRenderer Component
const MarkdownRenderer = ({ content }: { content: string }) => (
  <ReactMarkdown
    components={{
      p: ({ children }) => <p className="text-sm leading-relaxed mb-2">{children}</p>,
      h1: ({ children }) => <h1 className="text-xl font-bold mb-4 mt-2">{children}</h1>,
      h2: ({ children }) => <h2 className="text-lg font-bold mb-3 mt-2">{children}</h2>,
      h3: ({ children }) => <h3 className="text-base font-bold mb-2 mt-2">{children}</h3>,
      ul: ({ children }) => <ul className="list-disc ml-4 mb-4">{children}</ul>,
      ol: ({ children }) => <ol className="list-decimal ml-4 mb-4">{children}</ol>,
      li: ({ children }) => <li className="mb-1">{children}</li>,
      code: ({ inline, className, children }) => {
        if (inline) {
          return <code className=" rounded  font-mono text-sm">{children}</code>;
        }
        return (
          <pre className=" rounded-lg my-4 font-mono text-sm overflow-x-auto">
            <code className={className}>{children}</code>
          </pre>
        );
      },
      blockquote: ({ children }) => (
        <blockquote className="border-l-4 border-gray-400/50 pl-4 italic my-4">{children}</blockquote>
      ),
      a: ({ children, href }) => (
        <a href={href} className="text-blue-400 hover:underline" target="_blank" rel="noopener noreferrer">
          {children}
        </a>
      ),
      table: ({ children }) => (
        <div className="overflow-x-auto my-4">
          <table className="min-w-full border border-gray-700 rounded">{children}</table>
        </div>
      ),
      thead: ({ children }) => <thead className="">{children}</thead>,
      tr: ({ children }) => <tr className="border-b border-gray-700">{children}</tr>,
      th: ({ children }) => <th className="px-4 py-2 text-left border-r border-gray-700 last:border-r-0">{children}</th>,
      td: ({ children }) => <td className="px-4 py-2 border-r border-gray-700 last:border-r-0">{children}</td>,
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
    <div className="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-transparent">
      <div className="flex flex-col p-4 space-y-6">
        {messages.map((message, index) => {
          const isUser = message.startsWith("You:");
          const text = message.replace(/^(You:|AI:)\s*/, '');
          
          return (
            <div
              key={index}
              className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-fadeIn`}
            >
              <div
                className={`
                  relative group flex flex-col
                  max-w-[85%] rounded-2xl p-4
                  ${isUser
                    ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-br-sm'
                    : 'bg-gray-700 text-gray-100 rounded-bl-sm'
                  }
                  shadow-lg
                  transition-all duration-200
                  hover:shadow-xl
                `}
              >
                <div className="prose prose-invert max-w-none">
                  {isUser ? (
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{text}</p>
                  ) : (
                    <MarkdownRenderer content={text} />
                  )}
                </div>
              </div>
            </div>
          );
        })}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};
