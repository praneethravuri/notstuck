"use client";
import { ChatMessages } from "../components/common/ChatMessages";
import { ChatInput } from "../components/common/ChatInput";
import { ModelSelector } from "../components/common/ModelSelector";
import LoadingPage from "../components/common/LoadingPage";
import { MessageSquare } from "lucide-react";
import { useChatLogic } from "../hooks/useChatLogic";
import { useBackendHealth } from "../hooks/useBackendHealth";

export default function HomePage() {
  const { isBackendReady, error } = useBackendHealth();
  const {
    messages,
    isLoading,
    isUploading,
    modelName,
    setModelName,
    handleFileUpload,
    handleSendMessage,
  } = useChatLogic();

  // Show loading screen until backend is ready
  if (!isBackendReady) {
    return <LoadingPage error={error} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 flex flex-col">
      {/* Header */}
      <header className="border-b border-slate-800/50 backdrop-blur-sm bg-slate-950/80 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center shadow-lg shadow-violet-500/20">
              <MessageSquare className="h-5 w-5 text-white" />
            </div>
            <span className="font-bold text-xl text-white">NotStuck</span>
          </div>
          <ModelSelector modelName={modelName} setModelName={setModelName} />
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col max-w-5xl w-full mx-auto px-6">
        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto">
          <ChatMessages messages={messages} isLoading={isLoading} />
        </div>

        {/* Chat Input */}
        <div className="pb-6">
          <ChatInput
            onSendMessage={handleSendMessage}
            uploadHandler={handleFileUpload}
            isUploading={isUploading}
          />
        </div>
      </main>
    </div>
  );
}
