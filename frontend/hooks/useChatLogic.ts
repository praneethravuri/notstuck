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

            console.log("Upload response:", response.data);

            // Show detailed results
            const { message, files_processed, details } = response.data;
            const hasErrors = details?.some((d: string) => d.includes("❌") || d.toLowerCase().includes("error"));

            toast({
                title: hasErrors ? "Upload Completed with Issues" : "Upload Successful",
                description: message + (details ? "\n" + details.join("\n") : ""),
                variant: hasErrors ? "destructive" : "success",
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

            // Handle streaming response
            const reader = res.body?.getReader();
            const decoder = new TextDecoder();

            if (!reader) {
                throw new Error("No reader available");
            }

            let aiMessageIndex = -1;
            let accumulatedText = "";
            let sources: any[] = [];

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split("\n");

                for (const line of lines) {
                    if (line.startsWith("data: ")) {
                        const data = JSON.parse(line.substring(6));

                        if (data.type === "sources") {
                            sources = data.data;
                        } else if (data.type === "content") {
                            accumulatedText += data.data;

                            // Add or update AI message
                            setMessages((prev) => {
                                if (aiMessageIndex === -1) {
                                    aiMessageIndex = prev.length;
                                    return [...prev, { role: "ai", text: accumulatedText, sources }];
                                } else {
                                    const updated = [...prev];
                                    updated[aiMessageIndex] = { role: "ai", text: accumulatedText, sources };
                                    return updated;
                                }
                            });
                        } else if (data.type === "error") {
                            throw new Error(data.data);
                        }
                    }
                }
            }
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
