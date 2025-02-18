"use client";
import React, { useEffect, useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "../ui/button";
import { ScrollArea } from "../ui/scroll-area";

interface Chat {
  chatId: string;
  name?: string;
  created_at?: string;
}

interface ChatListProps {
  onSelectChat: (chatId: string) => void;
  onNewChat: () => void;
}

export const ChatList: React.FC<ChatListProps> = ({ onSelectChat, onNewChat }) => {
  const [chats, setChats] = useState<Chat[]>([]);
  const [selectedChatId, setSelectedChatId] = useState<string | null>(null);

  const loadChats = async () => {
    try {
      const res = await fetch("/api/chats");
      if (!res.ok) throw new Error("Failed to fetch chats");
      const data = await res.json();
      setChats(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadChats();
  }, []);

  const handleChatSelect = (chatId: string) => {
    setSelectedChatId(chatId);
    onSelectChat(chatId);
  };

  const truncateText = (text: string, maxLength: number = 20) => {
    if (text.length <= maxLength) return text;
    return text.slice(0, maxLength) + "...";
  };

  return (
    <div className="flex flex-col space-y-4 p-4">
      <Button
        onClick={onNewChat}
        className="w-full py-6 gap-2 bg-stone-900 hover:bg-stone-800 border-gray-800 text-gray-200 hover:text-white transition-all duration-200"
        variant="outline"
      >
        <Plus className="h-5 w-5" />
        <span className="font-medium text-base">New Chat</span>
      </Button>
      <ScrollArea className="h-[280px]">
        <div className="space-y-2 pr-4">
          {chats.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 space-y-4">
              <div className="w-12 h-12 rounded-full bg-stone-800 flex items-center justify-center">
                <Plus className="h-6 w-6 text-gray-400" />
              </div>
              <div className="space-y-1 text-center">
                <p className="text-sm font-medium text-gray-300">No chat history yet</p>
                <p className="text-xs text-gray-500">Start a new conversation to get started</p>
              </div>
            </div>
          ) : (
            chats.map((chat) => (
              <button
                key={chat.chatId}
                onClick={() => handleChatSelect(chat.chatId)}
                className={`w-full text-left p-2 rounded-lg hover:bg-stone-800 transition-all duration-200 ${
                  selectedChatId === chat.chatId
                    ? "border-green-500/50 bg-green-500/10 text-green-500 hover:bg-green-500/10"
                    : ""
                }`}
              >
                <div className="flex flex-col space-y-1">
                  <span className="text-sm font-medium block truncate">
                    {truncateText(chat.name ? chat.name : `Chat ${chat.chatId.slice(-5)}`)}
                  </span>
                </div>
              </button>
            ))
          )}
        </div>
      </ScrollArea>
    </div>
  );
};
