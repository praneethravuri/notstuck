"use client";

import { useState, useEffect } from "react";
import { ChatMessages } from "@/components/chat/ChatMessages";
import { ChatInput } from "@/components/chat/ChatInput";
import CustomSidebar from "@/components/sidebar/CustomSidebar";
import { SettingsSection } from "@/components/model-settings/SettingsSection";
import axios from "axios";

interface PdfFile {
  name: string;
}

export default function ChatLayout() {
  // Chat messages state
  const [messages, setMessages] = useState<string[]>([]);

  // Settings state
  const [similarityThreshold, setSimilarityThreshold] = useState([0.7]);
  const [similarResults, setSimilarResults] = useState([7]);
  const [temperature, setTemperature] = useState([0.5]);
  const [maxTokens, setMaxTokens] = useState([2000]);
  const [responseStyle, setResponseStyle] = useState("detailed");

  // Sidebar data state
  const [files, setFiles] = useState<PdfFile[]>([]);
  const [sources, setSources] = useState<string[]>([]);

  // Fetch PDF files via Next.js API route
  useEffect(() => {
    async function loadFiles() {
      try {
        const res = await fetch("/api/get-pdfs");
        if (!res.ok) throw new Error("Failed to fetch PDF list");
        const data = await res.json();
        setFiles(data.files.map((filename: string) => ({ name: filename })));
      } catch (err) {
        console.error("Error fetching PDF list:", err);
      }
    }
    loadFiles();
  }, []);

  // Simulate fetching active context sources.
  useEffect(() => {
    async function fetchSources() {
      const exampleSources = ["doc1.pdf", "report.pdf"];
      setSources(exampleSources);
    }
    fetchSources();
  }, []);

  // Handle file upload
  const handleFileUpload = async (files: FileList) => {
    try {
      const formData = new FormData();
      Array.from(files).forEach((file) => {
        formData.append("files", file);
      });

      const response = await axios.post("http://127.0.0.1:8000/api/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      console.log("Upload successful:", response.data);
    } catch (error) {
      console.error("Upload failed:", error);
    }
  };

  // Handle sending a chat message
  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;
    setMessages((prev) => [...prev, `You: ${message}`]);

    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: message,
          similarityThreshold: similarityThreshold[0],
          similarResults: similarResults[0],
          temperature: temperature[0],
          maxTokens: maxTokens[0],
          responseStyle: responseStyle,
        }),
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
    <div className="h-screen w-full flex bg-stone-950">
      {/* Left Sidebar - Fixed */}
      <aside className="w-64 border-r border-gray-800 fixed left-0 top-0 bottom-0 h-screen overflow-hidden">
        <CustomSidebar files={files} sources={sources} uploadHandler={handleFileUpload} />
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col ml-64 mr-80">
        {/* Chat Messages - Only This Scrolls */}
        <div className="flex-1 overflow-y-auto p-4">
          <ChatMessages messages={messages} />
        </div>

        {/* Chat Input - Fixed at Bottom */}
        <div className="fixed bottom-0 left-64 right-80 bg-stone-950 p-4 ">
          <ChatInput onSendMessage={handleSendMessage} />
        </div>
      </main>

      {/* Right Sidebar - Fixed */}
      <aside className="w-80 border-l border-gray-800 fixed right-0 top-0 bottom-0 h-screen overflow-hidden">
        <SettingsSection
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
      </aside>
    </div>
  );
}
