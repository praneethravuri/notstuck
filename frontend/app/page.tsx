"use client";

import { useRouter } from "next/navigation";
import { Button } from "../components/ui/button";
import { MessageSquare, ArrowRight, Database, Zap, Shield } from "lucide-react";

export default function Home() {
  const router = useRouter();

  const handleNewChat = () => {
    router.push("/chat");
  };

  return (
    <div className="min-h-screen bg-stone-950 overflow-hidden">
      {/* Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-green-500/10 via-transparent to-purple-500/10" />

      {/* Hero Section */}
      <div className="relative">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-32">
          <div className="text-center">
            <div className="flex items-center justify-center mb-6 gap-2">
              <div className="w-12 h-12 bg-green-600 rounded-xl flex items-center justify-center">
                <MessageSquare className="h-6 w-6 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-green-500">NotStuck</h2>
            </div>

            <h1 className="text-5xl sm:text-6xl font-bold text-white mb-6 tracking-tight">
              Your Knowledge,{" "}
              <span className="bg-gradient-to-r from-green-400 to-emerald-500 text-transparent bg-clip-text">
                Enhanced
              </span>
            </h1>

            <p className="text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto mb-8">
              Transform your documents into intelligent conversations. Get unstuck with
              AI-powered insights and answers from your knowledge base.
            </p>

            <div className="flex items-center justify-center gap-4">
              <Button
                onClick={handleNewChat}
                className="bg-green-600 hover:bg-green-700 text-white px-8 py-6 rounded-xl font-semibold text-lg group transition-all duration-200 flex items-center gap-2"
              >
                Start Chatting
                <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="relative border-t border-gray-800">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 rounded-xl bg-gray-900/50 backdrop-blur-sm">
              <div className="w-10 h-10 bg-green-600/20 rounded-lg flex items-center justify-center mb-4">
                <Database className="h-5 w-5 text-green-500" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Knowledge Base</h3>
              <p className="text-gray-400">
                Upload your documents and transform them into an interactive knowledge base.
              </p>
            </div>

            <div className="p-6 rounded-xl bg-gray-900/50 backdrop-blur-sm">
              <div className="w-10 h-10 bg-green-600/20 rounded-lg flex items-center justify-center mb-4">
                <Zap className="h-5 w-5 text-green-500" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Instant Answers</h3>
              <p className="text-gray-400">
                Get immediate, contextual responses powered by advanced AI technology.
              </p>
            </div>

            <div className="p-6 rounded-xl bg-gray-900/50">
              <div className="w-10 h-10 bg-green-600/20 rounded-lg flex items-center justify-center mb-4">
                <Shield className="h-5 w-5 text-green-500" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Secure & Private</h3>
              <p className="text-gray-400">
                Your documents remain private and secure with advanced encryption.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Background Decoration */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]" />
      </div>
    </div>
  );
}
