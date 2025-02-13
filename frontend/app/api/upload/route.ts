// app/api/upload/route.ts
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    // Get the form data from the incoming request
    const formData = await request.formData();
    
    // Get the backend URL from environment variable
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    
    if (!backendUrl) {
      throw new Error('Backend URL not configured');
    }

    // Forward the request to the backend
    const response = await fetch(`${backendUrl}/api/upload`, {
      method: 'POST',
      body: formData, // Forward the FormData object directly
    });

    if (!response.ok) {
      throw new Error(`Backend responded with status: ${response.status}`);
    }

    const data = await response.json();

    return NextResponse.json({
      message: 'Files uploaded successfully',
      ...data
    }, { status: 200 });

  } catch (error) {
    console.error('Error uploading file:', error);
    return NextResponse.json(
      { error: 'Error uploading file' },
      { status: 500 }
    );
  }
}

export const config = {
  api: {
    bodyParser: false, // Disable the default body parser for file uploads
  },
};