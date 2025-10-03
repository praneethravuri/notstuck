// app/api/health/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Get the backend URL from environment variable
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    if (!backendUrl) {
      throw new Error('Backend URL not configured');
    }

    // Check backend health
    const response = await fetch(`${backendUrl}/health`, {
      method: 'GET',
      cache: 'no-cache',
    });

    if (!response.ok) {
      throw new Error(`Backend health check failed: ${response.status}`);
    }

    const data = await response.json();

    return NextResponse.json(data, { status: 200 });

  } catch (error) {
    console.error('Backend health check error:', error);
    return NextResponse.json(
      { status: 'unhealthy', error: 'Backend not reachable' },
      { status: 503 }
    );
  }
}
