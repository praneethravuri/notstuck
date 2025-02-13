import React, { useRef, useEffect } from "react";
import ReactMarkdown from 'react-markdown';
import { Loader2 } from "lucide-react";

export const ChatMessages = ({ messages, isLoading }: { messages: string[], isLoading: boolean }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <>
      {/* Fixed Header */}
      {/* <div className="fixed top-0 left-0 right-0 bg-stone-950 z-10 border-b border-gray-800">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <div className="text-center space-y-2">
            <h1 className="text-2xl font-semibold text-gray-200">Hey Oleve! 👋</h1>
            <p className="text-sm text-gray-400">Ask me anything about your documents</p>
          </div>
        </div>
      </div> */}

      {/* Scrollable Messages Area */}
      <div className="flex-1 overflow-y-auto h-[calc(100vh-8rem)] mt-24">
        <div className="max-w-4xl mx-auto px-4">
          <div className="flex flex-col space-y-6 pb-24">
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
                        ? 'bg-green-600 text-white shadow-lg shadow-green-900/20'
                        : 'bg-stone-900 border border-gray-800 text-gray-200'
                      }
                    `}
                  >
                    {isUser ? (
                      <p className="text-sm leading-relaxed whitespace-pre-wrap">{text}</p>
                    ) : (
                      <div className="prose prose-invert max-w-none">
                        <ReactMarkdown>{text}</ReactMarkdown>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}

            {isLoading && (
              <div className="flex justify-start">
                <div className="max-w-[85%] rounded-xl p-4 bg-stone-900 border border-gray-800">
                  <div className="flex items-center gap-3">
                    <Loader2 className="h-4 w-4 text-green-500 animate-spin" />
                    <p className="text-sm text-gray-400">NotStuck is thinking...</p>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>
    </>
  );
};