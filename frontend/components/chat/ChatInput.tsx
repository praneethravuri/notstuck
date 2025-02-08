import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { SendIcon } from "lucide-react"

interface ChatInputProps {
  onSendMessage: (message: string) => void
}

export default function ChatInput({ onSendMessage }: ChatInputProps) {
  const [inputValue, setInputValue] = useState("")

  const handleSend = () => {
    onSendMessage(inputValue)
    setInputValue("")
  }

  return (
    <div className="p-4 border-t border-gray-800 bg-black">
      <div className="flex space-x-2 max-w-4xl mx-auto">
        <Input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message..."
          className="bg-zinc-800 border-gray-800 focus:border-gray-700"
          onKeyPress={(e) => e.key === "Enter" && handleSend()}
        />
        <Button
          onClick={handleSend}
          className="bg-zinc-900 hover:bg-zinc-800 text-white"
        >
          <SendIcon className="h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}
