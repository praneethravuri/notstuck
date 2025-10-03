import { NextRequest, NextResponse } from "next/server";

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
