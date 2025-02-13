"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import { ChatMessages } from "../../components/chat/ChatMessages";
import { ChatInput } from "../../components/chat/ChatInput";
import CustomSidebar from "../../components/sidebar/CustomSidebar";
import { SettingsSection } from "../../components/model-settings/SettingsSection";
import { DocumentsSection } from "../../components/information/DocumentSection";
import { SourcesSection } from "../../components/information/SourcesSection";
import { UploadSection } from "../../components/information/UploadSection";
import ChatList from "../../components/chat/ChatList";
import { MessageSquare } from "lucide-react";
import { useToast } from "../../hooks/use-toast";
import { useRouter } from "next/navigation";

interface PdfFile {
  name: string;
}

// const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
// console.log(`API Url: ${apiUrl}`)

export default function ChatLayout() {
  const [messages, setMessages] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [chatId, setChatId] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [similarityThreshold, setSimilarityThreshold] = useState([0.7]);
  const [similarResults, setSimilarResults] = useState([7]);
  const [temperature, setTemperature] = useState([0.7]);
  const [maxTokens, setMaxTokens] = useState([5000]);
  const [responseStyle, setResponseStyle] = useState("detailed");
  const [modelName, setModelName] = useState("gpt-4o");
  const [files, setFiles] = useState<PdfFile[]>([]);
  const [sources, setSources] = useState<string[]>([]);
  const [relevantChunks, setRelevantChunks] = useState<string[]>([]);

  const { toast } = useToast();
  const router = useRouter();

  const handleNewChat = () => {
    setChatId(null);
    setMessages([]);
    router.push("/chat");
  };

  const loadChatHistory = async (chatId: string) => {
    try {
      const res = await fetch(`/api/chats/${chatId}`);
      if (!res.ok) throw new Error("Failed to fetch chat history");
      const data = await res.json();
      const formatted = data.messages.map((msg: { role: string; content: string }) =>
        msg.role === "user" ? `You: ${msg.content}` : `AI: ${msg.content}`
      );
      setMessages(formatted);
    } catch (error) {
      console.error("Error loading chat history:", error);
      toast({
        title: "Error",
        description: "Failed to load chat history",
        variant: "destructive",
      });
    }
  };

  const handleSelectChat = (selectedChatId: string) => {
    setChatId(selectedChatId);
    loadChatHistory(selectedChatId);
  };

  const loadFiles = async () => {
    try {
      const res = await fetch("/api/get-pdfs");
      if (!res.ok) throw new Error("Failed to fetch PDF list");
      const data = await res.json();
      setFiles(data.files.map((filename: string) => ({ name: filename })));
    } catch (err) {
      console.error("Error fetching PDF list:", err);
      toast({
        title: "Error",
        description: "Failed to fetch PDF list",
        variant: "destructive",
      });
    }
  };

  useEffect(() => {
    loadFiles();
  }, []);

  const handleFileUpload = async (files: FileList) => {
    setIsUploading(true);
    toast({
      title: "Uploading File",
      description: "Your file is being uploaded and your knowledge is expanding...",
    });

    try {
      const formData = new FormData();
      Array.from(files).forEach((file) => {
        formData.append("files", file);
      });

      const response = await axios.post(`${apiUrl}/api/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      console.log("Upload is successful:", response.data);

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
      setIsUploading(false);
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
          chatId: chatId,
        }),
      });

      if (!res.ok) {
        throw new Error(`Failed to get answer. Status: ${res.status}`);
      }

      const data = await res.json();
      setMessages((prev) => [...prev, `AI: ${data.answer}`]);
      setRelevantChunks(data.relevant_chunks);
      setSources(data.source_files);
    } catch (error) {
      console.error("Error fetching from /api/ask:", error);
      setMessages((prev) => [...prev, "Error: Could not fetch answer"]);
      toast({
        title: "Error",
        description: "Failed to fetch answer",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-stone-950 flex flex-col md:flex-row">
      {/* Left Sidebar */}
      <aside className="w-full md:w-64  border-r border-gray-800">
        <CustomSidebar>
          <div className="p-4 flex items-center space-x-2">
            <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
              <MessageSquare className="h-5 w-5 text-white" />
            </div>
            <span className="font-semibold text-gray-200">NotStuck</span>
          </div>
          <ChatList onSelectChat={handleSelectChat} onNewChat={handleNewChat} />
          <SourcesSection relevantChunks={relevantChunks} sources={sources} />
          <UploadSection uploadHandler={handleFileUpload} isUploading={isUploading} />
        </CustomSidebar>
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 p-4 flex flex-col">
        <div className="flex-1 overflow-y-auto">
          <ChatMessages messages={messages} isLoading={isLoading} />
        </div>
        <div className="mt-4">
          <ChatInput onSendMessage={handleSendMessage} />
        </div>
      </main>

      {/* Right Sidebar */}
      <aside className="w-full md:w-64 border-t md:border-t-0 md:border-l border-gray-800">
        <CustomSidebar>
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
          <DocumentsSection files={files} />
          
        </CustomSidebar>
      </aside>
    </div>
  );
}
