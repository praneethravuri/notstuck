// frontend/components/ChatList.tsx
"use client";
import React, { useEffect, useState } from "react";

interface Chat {
  chatId: string;
  created_at?: string;
  // You may also include other summary info (like the last message) if desired.
}

interface ChatListProps {
  onSelectChat: (chatId: string) => void;
}

const ChatList: React.FC<ChatListProps> = ({ onSelectChat }) => {
  const [chats, setChats] = useState<Chat[]>([]);

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

  return (
    <div className="p-4 border-b border-gray-800">
      <h2 className="text-sm font-semibold text-gray-200 mb-2">Chats</h2>
      {chats.length === 0 ? (
        <p className="text-xs text-gray-400">No chats available</p>
      ) : (
        chats.map((chat) => (
          <div
            key={chat.chatId}
            className="cursor-pointer text-xs text-gray-200 hover:text-green-600 mb-1"
            onClick={() => onSelectChat(chat.chatId)}
          >
            Chat {chat.chatId.slice(-5)}
          </div>
        ))
      )}
    </div>
  );
};

export default ChatList;
