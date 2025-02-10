// app/api/upload/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    // Note: Do not call req.json() here because that will parse the body and ruin the multipart form-data.
    // Instead, forward the raw body.
    const contentType = req.headers.get("content-type") || "";
    
    const backendResponse = await fetch("http://127.0.0.1:8000/api/upload", {
      method: "POST",
      headers: {
        "content-type": contentType,
      },
      // The req.body is a ReadableStream (in Next.js 13 with app directory)
      body: req.body,
    });

    if (!backendResponse.ok) {
      throw new Error("Failed to upload files to FastAPI");
    }
    const data = await backendResponse.json();
    return NextResponse.json(data);
  } catch (error: unknown) {
    console.error("Error in POST /api/upload:", error);
    let errorMessage = "An unexpected error occurred";
    if (error instanceof Error) {
      errorMessage = error.message;
    }
    return NextResponse.json({ error: errorMessage }, { status: 500 });
  }
}
