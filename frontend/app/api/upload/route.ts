import { NextRequest, NextResponse } from "next/server";
import axios from "axios";

export async function POST(req: NextRequest) {
  try {
    const contentType = req.headers.get("content-type") || "";

    // Forward the request to FastAPI using Axios
    const backendResponse = await axios.post("http://127.0.0.1:8000/api/upload", req.body, {
      headers: {
        "Content-Type": contentType,
      },
      responseType: "json",
    });

    return NextResponse.json(backendResponse.data);
  } catch (error) {
    console.error("Error in POST /api/upload:", error);
    return NextResponse.json(
      { error: "Failed to upload file to FastAPI" },
      { status: 500 }
    );
  }
}
