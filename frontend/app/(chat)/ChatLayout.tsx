"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import { ChatMessages } from "@/components/chat/ChatMessages";
import { ChatInput } from "@/components/chat/ChatInput";
import CustomSidebar from "@/components/sidebar/CustomSidebar";
import { SettingsSection } from "@/components/model-settings/SettingsSection";
import { useToast } from "@/hooks/use-toast";

interface PdfFile {
  name: string;
}

export default function ChatLayout() {
  // Chat messages state
  const [messages, setMessages] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Loading state for file uploads
  const [, setUploading] = useState(false);

  // Settings state
  const [similarityThreshold, setSimilarityThreshold] = useState([0.7]);
  const [similarResults, setSimilarResults] = useState([7]);
  const [temperature, setTemperature] = useState([0.7]);
  const [maxTokens, setMaxTokens] = useState([5000]);
  const [responseStyle, setResponseStyle] = useState("detailed");
  const [modelName, setModelName] = useState("gpt-4o");

  // Sidebar data state
  const [files, setFiles] = useState<PdfFile[]>([]);
  const [sources, setSources] = useState<string[]>([]);
  // New state for relevant chunks from the backend
  const [relevantChunks, setRelevantChunks] = useState<string[]>([]);

  const { toast } = useToast();

  const loadFiles = async () => {
    try {
      const res = await fetch("/api/get-pdfs");
      if (!res.ok) throw new Error("Failed to fetch PDF list");
      const data = await res.json();
      setFiles(data.files.map((filename: string) => ({ name: filename })));
    } catch (err) {
      console.error("Error fetching PDF list:", err);
    }
  };

  useEffect(() => {
    loadFiles();
  }, []);

  const handleFileUpload = async (files: FileList) => {
    setUploading(true);
    toast({
      title: "Uploading File",
      description: "Your file is being uploaded and your knowledge is expanding...",
    });

    try {
      const formData = new FormData();
      Array.from(files).forEach((file) => {
        formData.append("files", file);
      });

      const response = await axios.post("http://127.0.0.1:8000/api/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      console.log("Upload successful:", response.data);

      toast({
        title: "Upload Successful",
        description: "Your document has been uploaded successfully.",
      });

      loadFiles();
    } catch (error) {
      console.error("Upload failed:", error);
      toast({
        title: "Upload Failed",
        description: "There was an error uploading your document.",
        variant: "destructive",
      });
    } finally {
      setUploading(false);
    }
  };

  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;
    setMessages((prev) => [...prev, `You: ${message}`]);
    setIsLoading(true);

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
          modelName: modelName,
        }),
      });

      if (!res.ok) {
        throw new Error(`Failed to get answer. Status: ${res.status}`);
      }

      const data = await res.json();
      setMessages((prev) => [...prev, `AI: ${data.answer}`]);
      // Update the relevant chunks state from the backend response
      setRelevantChunks(data.relevant_chunks);
      console.log(data.source_files)
      setSources(data.source_files);
    } catch (error) {
      console.error("Error fetching from /api/ask:", error);
      setMessages((prev) => [...prev, "Error: Could not fetch answer"]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-screen w-full flex bg-stone-950">
      {/* Left Sidebar - Fixed */}
      <aside className="w-64 border-r border-gray-800 fixed left-0 top-0 bottom-0 h-screen overflow-hidden">
        <CustomSidebar 
          files={files} 
          sources={sources} 
          uploadHandler={handleFileUpload}
          relevantChunks={relevantChunks} // Pass the relevant chunks here
        />
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col ml-64 mr-80">
        <div className="flex-1 overflow-y-auto p-4">
          <ChatMessages messages={messages} isLoading={isLoading} />
        </div>

        <div className="fixed bottom-0 left-64 right-80 bg-stone-950 p-4">
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
          modelName={modelName}
          setModelName={setModelName}
        />
      </aside>
    </div>
  );
}
