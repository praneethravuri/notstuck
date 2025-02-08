"use client"
import { SidebarProvider } from "@/components/ui/sidebar"
import ChatLayout from "@/components/chat/ChatLayout"

export default function Home() {
  return (
    <SidebarProvider>
      <ChatLayout />
    </SidebarProvider>
  )
}