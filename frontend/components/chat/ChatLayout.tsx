"use client"
import { useState } from "react"
import { Sidebar, SidebarContent } from "@/components/ui/sidebar"
import ChatMessages from "./ChatMessages"
import ChatInput from "./ChatInput"
import FileExplorer from "../sidebar/FileExplorer"

export default function ChatLayout() {
  const [messages, setMessages] = useState<string[]>([])

  const handleSendMessage = (message: string) => {
    if (message.trim()) {
      setMessages([...messages, message])
    }
  }

  return (
    <div className="flex h-screen w-full bg-black">
      <main className="flex-1 flex flex-col">
        <ChatMessages messages={messages} />
        <ChatInput onSendMessage={handleSendMessage} />
      </main>
      <Sidebar side="right" className="w-80 border-l border-gray-800">
        <SidebarContent>
          <FileExplorer />
        </SidebarContent>
      </Sidebar>
    </div>
  )
}