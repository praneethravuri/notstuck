"use client"
import { useState } from "react"
import { Sidebar, SidebarContent } from "@/components/ui/sidebar"
import { ChatMessages } from "./ChatMessages"
import { ChatInput } from "./ChatInput"
import LeftSidebar from "@/components/sidebar/LeftSidebar"
import RightSidebar from "@/components/sidebar/RightSidebar"

export default function ChatLayout() {
  const [messages, setMessages] = useState<string[]>([])

  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return

    // 1) Store the user's message
    setMessages((prev) => [...prev, `You: ${message}`])

    try {
      // 2) Send POST request to Next.js route -> which calls FastAPI
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: message }),
      })

      if (!res.ok) {
        throw new Error(`Failed to get answer. Status: ${res.status}`)
      }

      const data = await res.json()
      // data should look like { answer: "... from FastAPI ..." }

      // 3) Append AI's answer to the conversation
      setMessages((prev) => [...prev, `AI: ${data.answer}`])
    } catch (error) {
      console.error("Error fetching from /api/ask:", error)
      setMessages((prev) => [...prev, "Error: Could not fetch answer"])
    }
  }

  return (
    <div className="flex min-h-screen w-full bg-gray-900/50">
      {/* Left Sidebar */}
      <Sidebar side="left" className="w-80 flex-shrink-0 border-r border-gray-800 overflow-y-auto">
        <SidebarContent>
          <LeftSidebar />
        </SidebarContent>
      </Sidebar>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Greetings Header */}
        <div className="p-4 border-b border-gray-800">
          <h1 className="text-xl font-semibold text-gray-200">Hey Oleve!</h1>
          <p className="text-sm text-gray-400">How can I assist you today?</p>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto">
          <ChatMessages messages={messages} />
        </div>

        {/* Chat Input */}
        <ChatInput onSendMessage={handleSendMessage} />
      </main>

      {/* Right Sidebar */}
      <Sidebar side="right" className="w-80 flex-shrink-0 border-l border-gray-800 overflow-y-auto">
        <SidebarContent>
          <RightSidebar />
        </SidebarContent>
      </Sidebar>
    </div>
  )
}

