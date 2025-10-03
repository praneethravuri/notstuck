// src/hooks/useChatLogic.ts
import { useState } from "react";
import axios from "axios";
import { useToast } from "./use-toast";

export interface ChatMessage {
    role: "user" | "ai";
    text: string;
    sources?: {
        source_file: string;
        page_number?: number;
        text: string;
    }[];
}

export function useChatLogic() {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isUploading, setIsUploading] = useState(false);
    const [modelName, setModelName] = useState("openai/gpt-4o");
    const { toast } = useToast();

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
                body: JSON.stringify({ question: message, modelName }),
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
        isUploading,
        modelName,
        setModelName,
        handleFileUpload,
        handleSendMessage,
    };
}
