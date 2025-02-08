import { Accordion } from "@/components/ui/accordion"
import FileItem from "./FileItem"

const files = [
  { name: "Document 1", content: ["Content 1", "Content 2"] },
  { name: "Document 2", content: ["Content 3", "Content 4"] },
  { name: "Document 3", content: ["Content 5", "Content 6"] },
]

export default function FileExplorer() {
  return (
    <div className="p-4">
      <h2 className="text-lg font-semibold mb-4 text-gray-200">Files</h2>
      <Accordion type="single" collapsible className="w-full">
        {files.map((file, index) => (
          <FileItem key={index} file={file} index={index} />
        ))}
      </Accordion>
    </div>
  )
}
