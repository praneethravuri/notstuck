"use client";
import { ChatMessages } from "../../components/common/ChatMessages";
import { ChatInput } from "../../components/common/ChatInput";
import CustomSidebar from "../../components/common/CustomSidebar";
import { DocumentsSection } from "../../components/common/DocumentSection";
import {ChatList} from "../../components/common/ChatList";
import { ModelSelector } from "../../components/common/ModelSelector";
import { MessageSquare } from "lucide-react";
import { useChatLogic } from "../../hooks/useChatLogic";

export default function ChatLayout() {
  const {
    messages,
    isLoading,
    isUploading,
    modelName,
    files,
    setModelName,
    handleNewChat,
    handleSelectChat,
    handleFileUpload,
    handleSendMessage,
  } = useChatLogic();

  return (
    <div className="min-h-screen bg-stone-950 flex flex-col md:flex-row">
      {/* Left Sidebar */}
      <aside className="w-full md:w-64 border-t md:border-t-0 md:border-r border-gray-800 flex flex-col h-screen">
        <CustomSidebar>
          <div className="p-4 flex items-center space-x-2 border-b border-gray-800">
            <div className="h-10 w-10 rounded-lg bg-green-500/10 flex items-center justify-center">
              <MessageSquare className="h-5 w-5 text-green-600" />
            </div>
            <span className="font-semibold text-gray-200">!Stuck</span>
          </div>
          <div className="flex flex-col h-[calc(100vh-64px)]">
            <div className="flex-none">
              <ChatList onSelectChat={handleSelectChat} onNewChat={handleNewChat} />
            </div>
            <div className="flex-1 border-t border-gray-800">
              <DocumentsSection files={files} />
            </div>
          </div>
        </CustomSidebar>
      </aside>
      {/* Main Chat Area */}
      <main className="flex-1 p-4 flex flex-col">
        <ModelSelector modelName={modelName} setModelName={setModelName} />
        <div className="flex-1 overflow-y-auto">
          <ChatMessages messages={messages} isLoading={isLoading} />
        </div>
        <div className="mt-4">
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
