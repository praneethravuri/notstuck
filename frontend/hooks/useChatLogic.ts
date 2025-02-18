// src/hooks/useChatLogic.ts
import { useState, useEffect } from "react";
import axios from "axios";
import { useToast } from "./use-toast";
import { useRouter } from "next/navigation";

export interface ChatMessage {
    role: "user" | "ai";
    text: string;
    sources?: {
        source_file: string;
        page_number?: number;
        text: string;
    }[];
}

interface ChatApiMessage {
    role: string;
    content: string;
    sources?: {
        source_file: string;
        page_number?: number;
        text?: string;
        chunk?: string;
    }[];
}


interface PdfFile {
    name: string;
}

export function useChatLogic() {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [chatId, setChatId] = useState<string | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [modelName, setModelName] = useState("gpt-4o");
    const [files, setFiles] = useState<PdfFile[]>([]);
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
            const formatted: ChatMessage[] = (data.messages as ChatApiMessage[]).map(
                (msg) => {
                    const sourcesFormatted = msg.sources?.map((source) => ({
                        source_file: source.source_file,
                        page_number: source.page_number,
                        text: source.text || source.chunk || "",
                    }));
                    return {
                        role: msg.role === "user" ? "user" : "ai",
                        text: msg.content,
                        sources: sourcesFormatted,
                    };
                }
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
            title: "Uploading files...",
            description: "Starting to upload files and expand knowledge",
        });
        try {
            const formData = new FormData();
            Array.from(files).forEach((file) => formData.append("files", file));

            const response = await axios.post("/api/upload", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            console.log("Upload is successful:", response.data);
            toast({
                title: "Upload Successful",
                description: "Your document has been uploaded successfully.",
                variant: "success",
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
        setMessages((prev) => [...prev, { role: "user", text: message }]);
        setIsLoading(true);
        try {
            const res = await fetch("/api/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: message, modelName, chatId }),
            });
            if (!res.ok) {
                throw new Error(`Failed to get answer. Status: ${res.status}`);
            }
            const data = await res.json();
            setMessages((prev) => [
                ...prev,
                { role: "ai", text: data.answer, sources: data.sources_metadata },
            ]);
        } catch (error) {
            console.error("Error fetching from /api/ask:", error);
            setMessages((prev) => [
                ...prev,
                { role: "ai", text: "Error: Could not fetch answer" },
            ]);
            toast({
                title: "Error",
                description: "Failed to fetch answer",
                variant: "destructive",
            });
        } finally {
            setIsLoading(false);
        }
    };

    return {
        messages,
        isLoading,
        chatId,
        isUploading,
        modelName,
        files,
        setModelName,
        handleNewChat,
        handleSelectChat,
        handleFileUpload,
        handleSendMessage,
    };
}
