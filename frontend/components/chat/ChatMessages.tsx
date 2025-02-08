import { ScrollArea } from "@/components/ui/scroll-area";

interface ChatMessagesProps {
  messages: string[];
}

export default function ChatMessages({ messages }: ChatMessagesProps) {
  return (
    <ScrollArea className="flex-1 p-4">
      <div className="max-w-4xl mx-auto space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className="p-4 bg-gray-800/50 rounded-lg border border-gray-800 hover:border-gray-700 transition-colors backdrop-blur-sm 
            max-w-[50%] ml-auto"
          >
            <p className="text-gray-200 whitespace-pre-wrap">{message}</p>
          </div>
        ))}
      </div>
    </ScrollArea>
  );
}
