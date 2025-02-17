import React, { useEffect, useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "../../components/ui/button";
import { ScrollArea } from "../../components/ui/scroll-area";

interface Chat {
  chatId: string;
  name?: string;
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

  const truncateText = (text: string, maxLength: number = 20) => {
    if (text.length <= maxLength) return text;
    return text.slice(0, maxLength) + "...";
  };

  return (

          <div className="space-y-4 px-4">
            <Button 
              onClick={onNewChat}
              className="w-full h-10 gap-2"
              variant="outline"
            >
              <Plus className="h-4 w-4" />
              <span className="font-medium">New Chat</span>
            </Button>

            <ScrollArea className="h-[calc(100vh/3-6rem)]">
              <div className="space-y-2 pr-4">
                {chats.length === 0 ? (
                  <div className="text-center py-8 space-y-3">
                    <div className="space-y-1">
                      <p className="text-sm font-medium text-gray-300">No chat history yet</p>
                      <p className="text-xs text-gray-500">Start a new conversation</p>
                    </div>
                  </div>
                ) : (
                  chats.map((chat) => (
                    <button
                      key={chat.chatId}
                      onClick={() => handleChatSelect(chat.chatId)}
                      className={`w-full text-left px-4 py-3 rounded-lg border transition-all duration-200 ${
                        selectedChatId === chat.chatId
                          ? "border-green-500/50 bg-green-500/10 text-green-500 w-full"
                          : "border-gray-800 bg-stone-900/50 text-gray-400 hover:bg-stone-800"
                      }`}
                    >
                      <span className="text-sm font-medium block truncate">
                        {truncateText(chat.name ? chat.name : `Chat ${chat.chatId.slice(-5)}`)}
                      </span>
                    </button>
                  ))
                )}
              </div>
            </ScrollArea>
          </div>
  );
};

export default ChatList;