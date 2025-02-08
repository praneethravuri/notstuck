"use client";
import { useState, useEffect } from "react";
import { DocumentsSection } from "./DocumentSection";
import { SourcesSection } from "./SourcesSection";

const RightSidebar = () => {
    const [files, setFiles] = useState<{ name: string }[]>([]);
    const [sources, setSources] = useState<string[]>([]);

    // Fetch PDF files on component mount
    useEffect(() => {
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
    }, []);

    // Simulate updating sources (replace with actual API call)
    useEffect(() => {
        // Example: Fetch sources from an API or set them dynamically
        const fetchSources = async () => {
            // Replace with your API call to get active sources
            const exampleSources = ["doc1.pdf", "report.pdf"];
            setSources(exampleSources);
        };
        fetchSources();
    }, []);

    return (
        <div className="w-80 h-screen bg-gray-900/50 backdrop-blur-sm flex flex-col">
            {/* Documents Section */}
            <DocumentsSection files={files} />

            {/* Sources Section */}
            <SourcesSection sources={sources} />
        </div>
    );
};

export default RightSidebar;