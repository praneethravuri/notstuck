import React, { useRef, useEffect } from "react";
import ReactMarkdown from 'react-markdown';
import { Loader2, FileText, ChevronDown, ChevronUp } from "lucide-react";
import { Button } from "../../components/ui/button";

interface MessageSource {
  source_file: string;
  page_number?: number;
  chunk: string;
}

interface ChatMessagesProps {
  messages: string[];
  isLoading: boolean;
  sources: { source_file: string; page_number?: number; }[];
  relevantChunks: string[];
}

export const ChatMessages: React.FC<ChatMessagesProps> = ({ 
  messages, 
  isLoading, 
  sources, 
  relevantChunks 
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [expandedSources, setExpandedSources] = React.useState<{[key: number]: boolean}>({});

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const toggleSource = (messageIndex: number) => {
    setExpandedSources(prev => ({
      ...prev,
      [messageIndex]: !prev[messageIndex]
    }));
  };

  // Group sources with their chunks
  const getMessageSources = (messageIndex: number): MessageSource[] => {
    const aiMessageCount = messages.slice(0, messageIndex + 1).filter(msg => msg.startsWith("AI:")).length;
    if (aiMessageCount === 0) return [];
    
    const sourceStartIndex = (aiMessageCount - 1) * 3; // Assuming 3 sources per AI message
    const messageSources = sources.slice(sourceStartIndex, sourceStartIndex + 3);
    const messageChunks = relevantChunks.slice(sourceStartIndex, sourceStartIndex + 3);
    
    return messageSources.map((source, idx) => ({
      ...source,
      chunk: messageChunks[idx] || ""
    })).filter(source => source.chunk); // Only include sources with chunks
  };

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
              const messageSources = !isUser ? getMessageSources(index) : [];
              const hasExpandedSources = expandedSources[index];

              return (
                <div key={index} className="flex flex-col space-y-2">
                  <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
                    <div
                      className={`
                        max-w-[85%] rounded-xl p-4
                        ${isUser
                          ? 'bg-green-600 text-white shadow-lg shadow-green-900/20'
                          : ' text-gray-200'
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

                  {!isUser && messageSources.length > 0 && (
                    <div className="flex justify-start">
                      <div className="max-w-[85%] w-full pl-4">
                        <Button
                          variant="ghost"
                          onClick={() => toggleSource(index)}
                          className="w-full flex items-center justify-between px-4 py-2 text-sm text-gray-400 hover:text-gray-300 bg-stone-900/50 hover:bg-stone-900 rounded-lg transition-colors"
                        >
                          <span className="flex items-center gap-2">
                            <FileText className="h-4 w-4" />
                            {messageSources.length} {messageSources.length === 1 ? 'source' : 'sources'}
                          </span>
                          {hasExpandedSources ? (
                            <ChevronUp className="h-4 w-4" />
                          ) : (
                            <ChevronDown className="h-4 w-4" />
                          )}
                        </Button>

                        {hasExpandedSources && (
                          <div className="mt-2 space-y-2">
                            {messageSources.map((source, sourceIndex) => (
                              <div
                                key={sourceIndex}
                                className="bg-stone-900/30 rounded-lg border border-gray-800/50 overflow-hidden"
                              >
                                <div className="px-4 py-2 text-sm font-medium text-gray-400 border-b border-gray-800/50 bg-stone-900/30">
                                  {source.source_file}
                                  {source.page_number !== undefined && ` (Page ${source.page_number + 1})`}
                                </div>
                                <div className="px-4 py-3 text-sm text-gray-400">
                                  {source.chunk}
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  )}
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