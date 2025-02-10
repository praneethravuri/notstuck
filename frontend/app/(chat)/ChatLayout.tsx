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
        // Now calls the Next.js API route rather than FastAPI directly.
        const res = await fetch("/api/get-pdfs");
        if (!res.ok) throw new Error("Failed to fetch PDF list");
        const data = await res.json();
        // Assumes the API returns an object with a "files" array.
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
      // Replace this with a call to your own API if needed.
      const exampleSources = ["doc1.pdf", "report.pdf"];
      setSources(exampleSources);
    }
    fetchSources();
  }, []);

  // Custom upload handler using the Next.js API route
  // const handleFileUpload = async (files: FileList) => {
  //   try {
  //     const formData = new FormData();
  //     Array.from(files).forEach((file) => {
  //       formData.append("files", file);
  //     });

  //     // Instead of posting directly to FastAPI, post to our API route.
  //     const response = await axios.post("/api/upload", formData, {
  //       headers: { "Content-Type": "multipart/form-data" },
  //     });
  //     console.log("Upload successful:", response.data);
  //     // Optionally, you can refresh the file list here.
  //   } catch (error) {
  //     console.error("Upload failed:", error);
  //   }
  // };


  const handleFileUpload = async (files: FileList) => {
    try {
      const formData = new FormData();
      Array.from(files).forEach((file) => {
        formData.append("files", file);
      });

      const response = await axios.post("http://localhost:8000/api/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      console.log("Upload successful:", response.data);
      // Optionally, you can refresh your file list here.
    } catch (error) {
      console.error("Upload failed:", error);
    }
  };


  // Handle sending a chat message using the /api/ask route
  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;

    // Append the user's message to state
    setMessages((prev) => [...prev, `You: ${message}`]);

    try {
      // Now calling our own API route which forwards the request to FastAPI.
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
    <div className="flex min-h-screen w-full bg-gray-900/50">
      {/* Left Sidebar */}
      <aside className="w-64 border-r border-gray-800">
        <CustomSidebar files={files} sources={sources} uploadHandler={handleFileUpload} />
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="p-4 border-b border-gray-800">
          <h1 className="text-xl font-semibold text-gray-200">Hey Oleve!</h1>
          <p className="text-sm text-gray-400">How can I assist you today?</p>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4">
          <ChatMessages messages={messages} />
        </div>

        {/* Chat Input */}
        <div className="p-4 border-t border-gray-800">
          <ChatInput onSendMessage={handleSendMessage} />
        </div>
      </main>

      {/* Right Sidebar: Settings Section */}
      <aside className="w-80 border-l border-gray-800">
        <div className="p-4">
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
        </div>
      </aside>
    </div>
  );
}
