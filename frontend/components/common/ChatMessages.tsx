import React, { useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { Loader2, FileText, ChevronDown, ChevronUp } from "lucide-react";
import { Button } from "../../components/ui/button";

export interface MessageSource {
  source_file: string;
  page_number?: number;
  text: string;
}

export interface ChatMessage {
  role: "user" | "ai";
  text: string;
  sources?: MessageSource[];
}

interface GroupedSource {
  source_file: string;
  page_number?: number;
  texts: string[];
}

interface ChatMessagesProps {
  messages: ChatMessage[];
  isLoading: boolean;
}

export const ChatMessages: React.FC<ChatMessagesProps> = ({
  messages,
  isLoading,
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [expandedSources, setExpandedSources] = React.useState<{ [key: number]: boolean }>({});

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const toggleSource = (messageIndex: number) => {
    setExpandedSources((prev) => ({
      ...prev,
      [messageIndex]: !prev[messageIndex],
    }));
  };

  // Replace lodash's groupBy and orderBy with native JavaScript
  const groupSources = (sources: MessageSource[]): GroupedSource[] => {
    // Group sources by a composite key
    const grouped = sources.reduce((acc: Record<string, MessageSource[]>, source) => {
      const key = `${source.source_file}-${source.page_number ?? "no-page"}`;
      if (!acc[key]) {
        acc[key] = [];
      }
      acc[key].push(source);
      return acc;
    }, {});

    // Map the grouped object to an array of GroupedSource
    const groupedSources: GroupedSource[] = Object.values(grouped).map((group) => ({
      source_file: group[0].source_file,
      page_number: group[0].page_number,
      texts: group.map((source) => source.text),
    }));

    // Sort by source_file and then by page_number (undefined page_number goes last)
    groupedSources.sort((a, b) => {
      const fileCompare = a.source_file.localeCompare(b.source_file);
      if (fileCompare !== 0) return fileCompare;
      if (a.page_number === b.page_number) return 0;
      if (a.page_number === undefined) return 1;
      if (b.page_number === undefined) return -1;
      return a.page_number - b.page_number;
    });

    return groupedSources;
  };

  return (
    <div className="flex-1 overflow-y-auto h-[calc(100vh-16rem)] mt-16">
      <div className="max-w-4xl mx-auto px-4">
        {messages.length === 0 ? (
          <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center space-y-6 max-w-lg px-6">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-500/10 mb-2">
              <FileText className="h-8 w-8 text-green-500" />
            </div>
            <h1 className="text-4xl font-semibold text-gray-200">Hey Oleve! 👋</h1>
            <div className="space-y-4">
              <p className="text-gray-400 text-lg">
                I&apos;m here to help you understand your documents better.
              </p>
              <div className="bg-stone-900/50 rounded-xl p-6 border border-gray-800/50">
                <p className="text-gray-300 font-medium mb-3">Start by:</p>
                <ul className="text-gray-400 space-y-3">
                  <li className="flex items-start gap-2">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-green-500/10 text-green-500 flex items-center justify-center text-sm font-medium">
                      1
                    </span>
                    <span>Upload your documents using the upload section</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-green-500/10 text-green-500 flex items-center justify-center text-sm font-medium">
                      2
                    </span>
                    <span>Ask me any questions about your documents</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-green-500/10 text-green-500 flex items-center justify-center text-sm font-medium">
                      3
                    </span>
                    <span>Adjust the model settings to fine-tune responses</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex flex-col space-y-8 pb-24">
            {messages.map((message, index) => {
              const isUser = message.role === "user";
              const text = message.text;
              const messageSources = !isUser && message.sources ? message.sources : [];
              const hasExpandedSources = expandedSources[index];
              const groupedSources = groupSources(messageSources);

              return (
                <div key={index} className="flex flex-col space-y-3 group">
                  <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
                    <div
                      className={`
                        max-w-[85%] rounded-2xl p-5
                        ${isUser
                          ? "bg-green-600 text-white shadow-lg shadow-green-900/20"
                          : "bg-stone-900/30 text-gray-200 border border-gray-800/50"
                        }
                      `}
                    >
                      {isUser ? (
                        <p className="text-sm leading-relaxed whitespace-pre-wrap">
                          {text}
                        </p>
                      ) : (
                        <div className="prose prose-invert max-w-none">
                          <ReactMarkdown>{text}</ReactMarkdown>
                        </div>
                      )}
                    </div>
                  </div>

                  {!isUser && messageSources.length > 0 && (
                    <div className="flex justify-start">
                      <div className="max-w-[85%] w-full">
                        <Button
                          variant="ghost"
                          onClick={() => toggleSource(index)}
                          className="w-full flex items-center justify-between px-4 py-2.5 text-sm text-gray-400 hover:text-gray-300 bg-stone-900/50 hover:bg-stone-900 rounded-xl border border-gray-800/50 hover:border-gray-700/50 transition-all duration-200"
                        >
                          <span className="flex items-center gap-2">
                            <FileText className="h-4 w-4" />
                            {messageSources.length}{" "}
                            {messageSources.length === 1 ? "source" : "sources"}
                          </span>
                          {hasExpandedSources ? (
                            <ChevronUp className="h-4 w-4" />
                          ) : (
                            <ChevronDown className="h-4 w-4" />
                          )}
                        </Button>

                        {hasExpandedSources && (
                          <div className="mt-3 space-y-3">
                            {groupedSources.map((source, sourceIndex) => (
                              <div
                                key={sourceIndex}
                                className="bg-stone-900/30 rounded-xl border border-gray-800/50 overflow-hidden transition-all duration-200 hover:border-gray-700/50"
                              >
                                <div className="px-4 py-3 text-sm font-medium text-gray-400 border-b border-gray-800/50 bg-stone-900/30">
                                  <div className="flex items-center gap-2">
                                    <FileText className="h-4 w-4" />
                                    <span>{source.source_file}</span>
                                    {source.page_number !== undefined && (
                                      <span className="px-2 py-0.5 rounded-full bg-stone-800 text-xs">
                                        Page {source.page_number + 1}
                                      </span>
                                    )}
                                  </div>
                                </div>
                                <div className="px-4 py-3 text-sm text-gray-400 leading-relaxed">
                                  {source.texts.map((text, textIndex) => (
                                    <React.Fragment key={textIndex}>
                                      <p>{text}</p>
                                      {textIndex < source.texts.length - 1 && (
                                        <div className="my-2 border-t border-gray-700" />
                                      )}
                                    </React.Fragment>
                                  ))}
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
                <div className="max-w-[85%] rounded-xl p-4 bg-stone-900/30 border border-gray-800/50">
                  <div className="flex items-center gap-3">
                    <Loader2 className="h-4 w-4 text-green-500 animate-spin" />
                    <p className="text-sm text-gray-400">
                      NotStuck is thinking...
                    </p>
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

export default ChatMessages;
