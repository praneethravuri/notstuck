// frontend/app/api/startup-status/route.ts
import { NextResponse } from "next/server";

const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function GET() {
    try {
        // Call the FastAPI health-check
        const res = await fetch(`${apiUrl}/api/health-check`);
        const data = await res.json();
        // Forward the exact JSON to the client
        return NextResponse.json(data, { status: res.status });
    } catch (error) {
        // If there's a network error or something else
        console.error("Error calling health-check:", error);
        return NextResponse.json(
            { ready: false, error: "Failed to contact backend." },
            { status: 500 }
        );
    }
}
