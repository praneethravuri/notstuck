import { NextRequest, NextResponse } from "next/server";

const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function POST(req: NextRequest) {
    try {
        // Parse incoming data from the client, now including an optional chatId.
        const {
            question,
            similarityThreshold,
            similarResults,
            temperature,
            maxTokens,
            responseStyle,
            modelName,
            chatId  // New field!
        } = await req.json();

        // Forward the question and settings (including chatId, if available) to the FastAPI backend.
        const backendResponse = await fetch(`${apiUrl}/api/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ 
                question,
                similarityThreshold,
                similarResults,
                temperature,
                maxTokens,
                responseStyle,
                modelName,
                chatId,  // Forward the chat session ID
            }),
        });

        if (!backendResponse.ok) {
            console.error("FastAPI returned an error:", backendResponse.status, backendResponse.statusText);
            throw new Error("Error returned by FastAPI");
        }

        // Return the backend's JSON response to the client.
        const data = await backendResponse.json();
        return NextResponse.json(data);

    } catch (error: unknown) {
        console.error(error);
        let errorMessage = "An unexpected error occurred";
        if (error instanceof Error) {
            errorMessage = error.message;
        }
        return NextResponse.json({ error: errorMessage }, { status: 500 });
    }
}
