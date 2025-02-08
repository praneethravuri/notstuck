"use client";
import { useState } from "react";
import { Sidebar, SidebarContent } from "@/components/ui/sidebar";
import ChatMessages from "./ChatMessages";
import ChatInput from "./ChatInput";
import CustomSidebar from '@/components/sidebar/CustomSidebar';

export default function ChatLayout() {
  const [messages, setMessages] = useState<string[]>([]);

  const handleSendMessage = (message: string) => {
    if (message.trim()) {
      setMessages([...messages, message]);
    }
  };

  return (
    <div className="flex w-full bg-gray-900">
      <main className="flex-1 flex flex-col bg-gradient-to-b from-gray-900 to-black">
        <ChatMessages messages={messages} />
        <ChatInput onSendMessage={handleSendMessage} />
      </main>
      <Sidebar side="right" className="w-80 border-l border-gray-800">
        <SidebarContent>
          <CustomSidebar />
        </SidebarContent>
      </Sidebar>
    </div>
  );
}