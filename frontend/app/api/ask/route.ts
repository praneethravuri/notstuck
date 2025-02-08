import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
    try {
        // 1) Parse incoming data from the client
        const { question } = await req.json();

        // 2) Forward the question to the FastAPI backend
        //    (assuming it's running on localhost:8000)
        const backendResponse = await fetch("http://127.0.0.1:8000/api/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question }),
        });

        if (!backendResponse.ok) {
            // Log the status code or text for debugging
            console.error("FastAPI returned an error:", backendResponse.status, backendResponse.statusText);
            throw new Error("Error returned by FastAPI");
        }

        // 3) Return the backend's JSON to the client
        const data = await backendResponse.json();
        return NextResponse.json(data);

    } catch (error: any) {
        // Return an error response
        console.log(error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
