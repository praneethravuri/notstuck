import { useState } from "react";
import { Sidebar, SidebarContent } from "@/components/ui/sidebar";
import { ChatMessages } from "./ChatMessages";
import { ChatInput } from "./ChatInput";
import LeftSidebar from "@/components/sidebar/LeftSidebar";
import RightSidebar from "@/components/sidebar/RightSidebar";

export default function ChatLayout() {
  const [messages, setMessages] = useState([]);

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    setMessages((prev) => [...prev, `You: ${message}`]);

    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: message }),
      });

      if (!res.ok) {
        throw new Error(`Failed to get answer. Status: ${res.status}`);
      }

      const data = await res.json();
      setMessages((prev) => [...prev, `AI: ${data.answer}`]);
    } catch (error) {
      console.error("Error fetching from /api/ask:", error);
      setMessages((prev) => [...prev, "Error: Could not fetch answer"]);
    }
  };

  return (
    <div className="flex h-screen w-full overflow-hidden bg-gray-900">
      {/* Left Sidebar */}
      <Sidebar side="left" className="w-80 min-w-80 border-r border-gray-800">
        <SidebarContent>
          <div className="h-full overflow-y-auto">
            <LeftSidebar />
          </div>
        </SidebarContent>
      </Sidebar>

      {/* Main Chat Area */}
      <main className="flex flex-1 flex-col min-w-0 bg-gray-900">
        {/* Header */}
        <div className="flex-none p-4 border-b border-gray-800">
          <h1 className="text-xl font-semibold text-gray-200">Hey Oleve!</h1>
          <p className="text-sm text-gray-400">How can I assist you today?</p>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4">
          <ChatMessages messages={messages} />
        </div>

        {/* Input Area */}
        <div className="flex-none p-4 border-t border-gray-800">
          <ChatInput onSendMessage={handleSendMessage} />
        </div>
      </main>

      {/* Right Sidebar */}
      <Sidebar side="right" className="w-80 min-w-80 border-l border-gray-800">
        <SidebarContent>
          <div className="h-full overflow-y-auto">
            <RightSidebar />
          </div>
        </SidebarContent>
      </Sidebar>
    </div>
  );
}