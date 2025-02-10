// app/api/get-pdfs/route.ts
import { NextResponse } from "next/server";

export async function GET() {
  try {
    // Forward the request to the FastAPI backend.
    const backendResponse = await fetch("http://127.0.0.1:8000/api/get-pdfs");
    if (!backendResponse.ok) {
      throw new Error("Failed to fetch PDF list from FastAPI");
    }
    const data = await backendResponse.json();
    return NextResponse.json(data);
  } catch (error: unknown) {
    console.error("Error in GET /api/get-pdfs:", error);
    let errorMessage = "An unexpected error occurred";
    if (error instanceof Error) {
      errorMessage = error.message;
    }
    return NextResponse.json({ error: errorMessage }, { status: 500 });
  }
}
