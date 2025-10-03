import { NextRequest, NextResponse } from "next/server";

const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function GET(req: NextRequest) {
    try {
        // Fetch available models from backend
        const backendResponse = await fetch(`${apiUrl}/api/models`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
            cache: 'no-store', // Don't cache the models list
        });

        if (!backendResponse.ok) {
            console.error("Backend returned an error:", backendResponse.status, backendResponse.statusText);
            throw new Error("Error fetching models from backend");
        }

        const data = await backendResponse.json();
        return NextResponse.json(data);

    } catch (error: unknown) {
        console.error("Error fetching models:", error);
        let errorMessage = "Failed to fetch available models";
        if (error instanceof Error) {
            errorMessage = error.message;
        }
        return NextResponse.json({ error: errorMessage }, { status: 500 });
    }
}
