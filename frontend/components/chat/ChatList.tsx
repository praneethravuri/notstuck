import React, { useEffect, useState } from "react";
import { Plus, MessageSquare, MessagesSquare } from "lucide-react";
import { Button } from "../../components/ui/button";
import { ScrollArea } from "../../components/ui/scroll-area";
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "../../components/ui/accordion";

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
    <Accordion 
      type="single" 
      collapsible 
      defaultValue="chats"
      className="space-y-2"
    >
      <AccordionItem value="chats" className="border-none">
        <AccordionTrigger className="py-4 px-4 hover:no-underline hover:bg-stone-900/50">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-lg bg-green-500/10 flex items-center justify-center">
              <MessagesSquare className="h-4 w-4 text-green-500" />
            </div>
            <div>
              <h2 className="text-base font-medium text-gray-200">Chat History</h2>
            </div>
          </div>
        </AccordionTrigger>
        <AccordionContent>
          <div className="space-y-4 px-4">
            <Button 
              onClick={onNewChat}
              className="w-full bg-stone-900/50 border border-gray-800 hover:bg-stone-800 text-gray-200 h-10 gap-2"
            >
              <Plus className="h-4 w-4" />
              <span className="font-medium">New Chat</span>
            </Button>

            <ScrollArea className="h-[calc(100vh/3-6rem)]">
              <div className="space-y-2 pr-4">
                {chats.length === 0 ? (
                  <div className="text-center py-8 space-y-3">
                    <MessageSquare className="mx-auto h-12 w-12 text-gray-500/50" />
                    <div className="space-y-1">
                      <p className="text-sm font-medium text-gray-300">
                        No chat history yet
                      </p>
                      <p className="text-xs text-gray-500">
                        Start a new conversation
                      </p>
                    </div>
                  </div>
                ) : (
                  chats.map((chat) => (
                    <button
                      key={chat.chatId}
                      onClick={() => handleChatSelect(chat.chatId)}
                      className={`w-full group flex items-center justify-between p-3 rounded-lg border transition-all duration-200 ${
                        selectedChatId === chat.chatId
                          ? "border-green-500/50 bg-green-500/10 text-green-500"
                          : "border-gray-800 bg-stone-900/50 text-gray-400 hover:bg-stone-800"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <MessageSquare 
                          className={`h-4 w-4 ${
                            selectedChatId === chat.chatId
                              ? "text-green-500"
                              : "text-gray-500"
                          }`}
                        />
                        <span className="text-sm font-medium">
                          Chat {chat.chatId.slice(-5)}
                        </span>
                      </div>
                    </button>
                  ))
                )}
              </div>
            </ScrollArea>
          </div>
        </AccordionContent>
      </AccordionItem>
    </Accordion>
  );
};

export default ChatList;