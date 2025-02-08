import { ScrollArea } from "@/components/ui/scroll-area"

interface ChatMessagesProps {
  messages: string[]
}

export default function ChatMessages({ messages }: ChatMessagesProps) {
  return (
    <ScrollArea className="flex-1 p-4">
      {messages.map((message, index) => (
        <div
          key={index}
          className="mb-4 p-4 bg-gray-900 rounded-lg border border-gray-800 shadow-lg hover:border-gray-700 transition-colors"
        >
          {message}
        </div>
      ))}
    </ScrollArea>
  )
}