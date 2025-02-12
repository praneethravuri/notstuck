import React, { useEffect, useState } from "react";
import { Plus, MessageSquare } from "lucide-react";
import { Button } from "../../components/ui/button";

interface Chat {
  chatId: string;
  created_at?: string;
}

interface ChatListProps {
  onSelectChat: (chatId: string) => void;
  onNewChat: () => void;
}

const ChatList: React.FC<ChatListProps> = ({ onSelectChat, onNewChat }) => {
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

  return (
    <div className="flex flex-col h-full">
      <div className="p-4">
        <Button
          onClick={onNewChat}
          className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors duration-200"
        >
          <Plus className="h-4 w-4" />
          New Chat
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto px-2">
        <div className="space-y-1">
          {chats.length === 0 ? (
            <div className="text-center py-4">
              <MessageSquare className="h-8 w-8 mx-auto text-gray-400 mb-2 opacity-50" />
              <p className="text-sm text-gray-400">No chat history yet</p>
              <p className="text-xs text-gray-500">Start a new conversation</p>
            </div>
          ) : (
            chats.map((chat) => (
              <button
                key={chat.chatId}
                onClick={() => handleChatSelect(chat.chatId)}
                className={`w-full px-3 py-2 rounded-lg text-left transition-colors duration-200 ${
                  selectedChatId === chat.chatId
                    ? "bg-green-600/20 text-green-500"
                    : "text-gray-300 hover:bg-gray-800/50"
                }`}
              >
                <div className="flex items-center gap-2">
                  <MessageSquare className="h-4 w-4 flex-shrink-0" />
                  <span className="text-sm truncate">
                    Chat {chat.chatId.slice(-5)}
                  </span>
                </div>
                {chat.created_at && (
                  <span className="text-xs text-gray-500 ml-6">
                    {new Date(chat.created_at).toLocaleDateString()}
                  </span>
                )}
              </button>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatList;