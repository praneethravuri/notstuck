"use client";
import { useState, useEffect } from "react";
import { DocumentsSection } from "./DocumentSection";
import { SourcesSection } from "./SourcesSection";
import { SettingsSection } from './SettingSection';
import { UploadSection } from './UploadSection';

interface CustomSidebarProps {
    position: "left" | "right";
    similarityThreshold?: number[];
    setSimilarityThreshold?: (value: number[]) => void;
    similarResults?: number[];
    setSimilarResults?: (value: number[]) => void;
    temperature?: number[];
    setTemperature?: (value: number[]) => void;
    maxTokens?: number[];
    setMaxTokens?: (value: number[]) => void;
    responseStyle?: string;
    setResponseStyle?: (value: string) => void;
}

const CustomSidebar = ({
    position,
    similarityThreshold,
    setSimilarityThreshold,
    similarResults,
    setSimilarResults,
    temperature,
    setTemperature,
    maxTokens,
    setMaxTokens,
    responseStyle,
    setResponseStyle,
}: CustomSidebarProps) => {
    const [files, setFiles] = useState<{ name: string }[]>([]);
    const [sources, setSources] = useState<string[]>([]);

    // Fetch PDF files on component mount (only for right sidebar)
    useEffect(() => {
        if (position === "left") {
            async function loadFiles() {
                try {
                    const res = await fetch("http://localhost:8000/api/get-pdfs");
                    if (!res.ok) throw new Error("Failed to fetch PDF list");
                    const data = await res.json();
                    setFiles(data.files.map((filename: string) => ({ name: filename })));
                } catch (err) {
                    console.error("Error fetching PDF list:", err);
                }
            }
            loadFiles();
        }
    }, [position]);

    // Simulate updating sources (only for right sidebar)
    useEffect(() => {
        if (position === "left") {
            const fetchSources = async () => {
                const exampleSources = ["doc1.pdf", "report.pdf"];
                setSources(exampleSources);
            };
            fetchSources();
        }
    }, [position]);

    return (
        <div className="w-80 h-screen bg-gray-900/50 backdrop-blur-sm flex flex-col">
            {position === "right" ? (
                <>
                    {/* Settings Section */}
                    <SettingsSection
                        similarityThreshold={similarityThreshold!}
                        setSimilarityThreshold={setSimilarityThreshold!}
                        similarResults={similarResults!}
                        setSimilarResults={setSimilarResults!}
                        temperature={temperature!}
                        setTemperature={setTemperature!}
                        maxTokens={maxTokens!}
                        setMaxTokens={setMaxTokens!}
                        responseStyle={responseStyle!}
                        setResponseStyle={setResponseStyle!}
                    />
                    {/* Upload Section */}
                    <UploadSection />
                </>
            ) : (
                <>
                    {/* Documents Section */}
                    <DocumentsSection files={files} />
                    {/* Sources Section */}
                    <SourcesSection sources={sources} />
                </>
            )}
        </div>
    );
};

export default CustomSidebar;