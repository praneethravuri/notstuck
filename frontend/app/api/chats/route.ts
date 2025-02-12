// frontend/app/api/chats/route.ts
import { NextResponse } from "next/server";

// Ensure that your NEXT_PUBLIC_BACKEND_URL is set in your environment
const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function GET() {
  try {
    // Forward the GET request to the FastAPI endpoint for chats
    const backendResponse = await fetch(`${apiUrl}/api/chats`);
    if (!backendResponse.ok) {
      console.error("FastAPI returned an error:", backendResponse.status, backendResponse.statusText);
      throw new Error("Failed to fetch chats from FastAPI");
    }
    const data = await backendResponse.json();
    return NextResponse.json(data);
  } catch (error: unknown) {
    console.error("Error in GET /api/chats:", error);
    let errorMessage = "An unexpected error occurred";
    if (error instanceof Error) {
      errorMessage = error.message;
    }
    return NextResponse.json({ error: errorMessage }, { status: 500 });
  }
}
