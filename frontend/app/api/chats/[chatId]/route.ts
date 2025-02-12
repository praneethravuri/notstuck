// frontend/app/api/chats/[chatId]/route.ts
import { NextResponse } from "next/server";

const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function GET(request: Request, { params }: { params: { chatId: string } }) {
  const { chatId } = params;

  try {
    // Forward the GET request to your FastAPI backend for a specific chat.
    const backendResponse = await fetch(`${apiUrl}/api/chats/${chatId}`);
    if (!backendResponse.ok) {
      console.error("FastAPI returned an error:", backendResponse.status, backendResponse.statusText);
      throw new Error("Failed to fetch chat history from FastAPI");
    }
    const data = await backendResponse.json();
    return NextResponse.json(data);
  } catch (error: unknown) {
    console.error("Error in GET /api/chats/[chatId]:", error);
    let errorMessage = "An unexpected error occurred";
    if (error instanceof Error) {
      errorMessage = error.message;
    }
    return NextResponse.json({ error: errorMessage }, { status: 500 });
  }
}
