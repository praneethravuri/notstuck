import { NextRequest } from "next/server";

const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function POST(req: NextRequest) {
    try {
        // Parse incoming data from the client
        const {
            question,
            modelName
        } = await req.json();

        // Forward the question and settings to the FastAPI backend
        const backendResponse = await fetch(`${apiUrl}/api/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                question,
                modelName,
            }),
        });

        if (!backendResponse.ok) {
            console.error("FastAPI returned an error:", backendResponse.status, backendResponse.statusText);
            throw new Error("Error returned by FastAPI");
        }

        // Forward the streaming response directly to the client
        return new Response(backendResponse.body, {
            headers: {
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        });

    } catch (error: unknown) {
        console.error(error);
        let errorMessage = "An unexpected error occurred";
        if (error instanceof Error) {
            errorMessage = error.message;
        }
        return new Response(JSON.stringify({ error: errorMessage }), {
            status: 500,
            headers: { "Content-Type": "application/json" }
        });
    }
}
