import { AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { FileIcon } from "lucide-react"

interface FileItemProps {
  file: {
    name: string
    content: string[]
  }
  index: number
}

export default function FileItem({ file, index }: FileItemProps) {
  return (
    <AccordionItem value={`item-${index}`} className="border-gray-800">
      <AccordionTrigger className="hover:bg-gray-900 rounded-lg px-2">
        <div className="flex items-center space-x-2">
          <FileIcon className="h-4 w-4 text-gray-400" />
          <span>{file.name}</span>
        </div>
      </AccordionTrigger>
      <AccordionContent>
        <ul className="space-y-2 pl-6">
          {file.content.map((item, itemIndex) => (
            <li
              key={itemIndex}
              className="text-gray-400 hover:text-gray-200 cursor-pointer transition-colors"
            >
              {item}
            </li>
          ))}
        </ul>
      </AccordionContent>
    </AccordionItem>
  )
}