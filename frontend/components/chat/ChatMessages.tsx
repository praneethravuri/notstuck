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
    <div className="flex-1 overflow-y-auto h-[calc(100vh-8rem)] mt-24">
      <div className="max-w-4xl mx-auto px-4">
        {messages.length === 0 ? (
          <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center space-y-4 max-w-lg px-4">
            <h1 className="text-3xl font-semibold text-gray-200">Hey Oleve! 👋</h1>
            <div className="space-y-2">
              <p className="text-gray-400">I&apos;m here to help you understand your documents better.</p>
              <p className="text-gray-400">Start by:</p>
              <ul className="text-gray-400 space-y-2">
                <li>1. Upload your documents using the upload section</li>
                <li>2. Ask me any questions about your documents</li>
                <li>3. Adjust the model settings to fine-tune responses</li>
              </ul>
            </div>
          </div>
        ) : (
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
        )}
      </div>
    </div>
  );
};