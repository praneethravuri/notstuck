"use client"
import { useState } from "react"
import { ChatMessages } from "./ChatMessages"
import { ChatInput } from "./ChatInput"
import CustomSidebar from "../sidebar/CustomSidebar"

export default function ChatLayout() {
  const [messages, setMessages] = useState<string[]>([])

  // State for settings
  const [similarityThreshold, setSimilarityThreshold] = useState([0.7]);
  const [similarResults, setSimilarResults] = useState([7]);
  const [temperature, setTemperature] = useState([0.5]);
  const [maxTokens, setMaxTokens] = useState([2000]);
  const [responseStyle, setResponseStyle] = useState("detailed");

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
        body: JSON.stringify({
          question: message,
          similarityThreshold: similarityThreshold[0],
          similarResults: similarResults[0],
          temperature: temperature[0],
          maxTokens: maxTokens[0],
          responseStyle: responseStyle
        }),
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
      <CustomSidebar position="left" />

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Greetings Header */}
        <div className="p-4 border-b border-gray-800">
          <h1 className="text-xl font-semibold text-gray-200">Hey Oleve!</h1>
          <p className="text-sm text-gray-400">How can I assist you today?</p>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-hidden">
          <ChatMessages messages={messages} />
        </div>

        {/* Chat Input */}
        <ChatInput onSendMessage={handleSendMessage} />
      </main>

      {/* Right Sidebar */}
      
      <CustomSidebar
        position="right"
        similarityThreshold={similarityThreshold}
        setSimilarityThreshold={setSimilarityThreshold}
        similarResults={similarResults}
        setSimilarResults={setSimilarResults}
        temperature={temperature}
        setTemperature={setTemperature}
        maxTokens={maxTokens}
        setMaxTokens={setMaxTokens}
        responseStyle={responseStyle}
        setResponseStyle={setResponseStyle}
      />
    </div>
  )
}