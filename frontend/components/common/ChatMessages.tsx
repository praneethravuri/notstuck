import React, { useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { Loader2, FileText, ChevronDown, ChevronUp, Sparkles } from "lucide-react";
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

  const groupSources = (sources: MessageSource[]): GroupedSource[] => {
    const grouped = sources.reduce((acc: Record<string, MessageSource[]>, source) => {
      const key = `${source.source_file}-${source.page_number ?? "no-page"}`;
      if (!acc[key]) {
        acc[key] = [];
      }
      acc[key].push(source);
      return acc;
    }, {});

    const groupedSources: GroupedSource[] = Object.values(grouped).map((group) => ({
      source_file: group[0].source_file,
      page_number: group[0].page_number,
      texts: group.map((source) => source.text),
    }));

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
    <div className="flex-1 overflow-y-auto pb-4">
      <div className="max-w-4xl mx-auto">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-[60vh]">
            <div className="text-center space-y-6 max-w-lg px-6">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-violet-500/20 to-purple-600/20 border border-violet-500/20 mb-2">
                <Sparkles className="h-8 w-8 text-violet-400" />
              </div>
              <h1 className="text-3xl font-bold text-white">Welcome to NotStuck</h1>
              <div className="space-y-4">
                <p className="text-slate-400 text-base leading-relaxed">
                  Upload your documents and start asking questions to get intelligent, context-aware answers.
                </p>
                <div className="bg-slate-900/50 rounded-xl p-5 border border-slate-800/50">
                  <p className="text-slate-300 font-semibold mb-3 text-sm">Getting Started:</p>
                  <ul className="text-slate-400 space-y-2.5 text-sm">
                    <li className="flex items-start gap-3">
                      <span className="flex-shrink-0 w-6 h-6 rounded-full bg-gradient-to-br from-violet-500/20 to-purple-600/20 text-violet-400 flex items-center justify-center text-xs font-bold border border-violet-500/20">
                        1
                      </span>
                      <span>Upload documents to build your knowledge base</span>
                    </li>
                    <li className="flex items-start gap-3">
                      <span className="flex-shrink-0 w-6 h-6 rounded-full bg-gradient-to-br from-violet-500/20 to-purple-600/20 text-violet-400 flex items-center justify-center text-xs font-bold border border-violet-500/20">
                        2
                      </span>
                      <span>Ask questions about your documents</span>
                    </li>
                    <li className="flex items-start gap-3">
                      <span className="flex-shrink-0 w-6 h-6 rounded-full bg-gradient-to-br from-violet-500/20 to-purple-600/20 text-violet-400 flex items-center justify-center text-xs font-bold border border-violet-500/20">
                        3
                      </span>
                      <span>Get AI-powered insights with source references</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex flex-col space-y-6 py-6">
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
                        max-w-[85%] rounded-2xl px-5 py-4
                        ${isUser
                          ? "bg-gradient-to-br from-violet-600 to-purple-600 text-white shadow-lg shadow-violet-900/30"
                          : "bg-slate-900/50 text-slate-100 border border-slate-800/50 backdrop-blur-sm"
                        }
                      `}
                    >
                      {isUser ? (
                        <p className="text-sm leading-relaxed whitespace-pre-wrap font-medium">
                          {text}
                        </p>
                      ) : (
                        <div className="prose prose-invert max-w-none prose-sm prose-p:text-slate-200 prose-headings:text-white prose-a:text-violet-400 prose-code:text-violet-300 prose-pre:bg-slate-800">
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
                          className="w-full flex items-center justify-between px-4 py-2.5 text-sm text-slate-400 hover:text-slate-300 bg-slate-900/30 hover:bg-slate-900/50 rounded-xl border border-slate-800/50 hover:border-slate-700/50 transition-all duration-200"
                        >
                          <span className="flex items-center gap-2">
                            <FileText className="h-4 w-4 text-violet-400" />
                            <span className="font-medium">
                              {messageSources.length}{" "}
                              {messageSources.length === 1 ? "source" : "sources"}
                            </span>
                          </span>
                          {hasExpandedSources ? (
                            <ChevronUp className="h-4 w-4" />
                          ) : (
                            <ChevronDown className="h-4 w-4" />
                          )}
                        </Button>

                        {hasExpandedSources && (
                          <div className="mt-3 space-y-2.5">
                            {groupedSources.map((source, sourceIndex) => (
                              <div
                                key={sourceIndex}
                                className="bg-slate-900/30 rounded-xl border border-slate-800/50 overflow-hidden transition-all duration-200 hover:border-slate-700/50"
                              >
                                <div className="px-4 py-3 text-sm font-medium text-slate-300 border-b border-slate-800/50 bg-slate-900/30">
                                  <div className="flex items-center gap-2">
                                    <FileText className="h-4 w-4 text-violet-400" />
                                    <span className="font-semibold">{source.source_file}</span>
                                    {source.page_number !== undefined && (
                                      <span className="px-2 py-0.5 rounded-full bg-slate-800/50 text-xs text-slate-400 border border-slate-700/50">
                                        Page {source.page_number + 1}
                                      </span>
                                    )}
                                  </div>
                                </div>
                                <div className="px-4 py-3 text-sm text-slate-400 leading-relaxed">
                                  {source.texts.map((text, textIndex) => (
                                    <React.Fragment key={textIndex}>
                                      <p>{text}</p>
                                      {textIndex < source.texts.length - 1 && (
                                        <div className="my-2.5 border-t border-slate-800/50" />
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
                <div className="max-w-[85%] rounded-2xl px-5 py-4 bg-slate-900/50 border border-slate-800/50 backdrop-blur-sm">
                  <div className="flex items-center gap-3">
                    <Loader2 className="h-4 w-4 text-violet-400 animate-spin" />
                    <p className="text-sm text-slate-300 font-medium">
                      Thinking...
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
