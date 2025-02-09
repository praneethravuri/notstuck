// // app/api/get-pdfs/route.ts

// import { NextResponse } from "next/server";
// import fs from "fs/promises";
// import path from "path";

// export async function GET(request: Request) {
//   try {
//     // Adjust the directory as needed. Here we assume the PDFs are in "<project-root>/data/processed"
//     const processedDir = path.join(process.cwd(), "data", "processed");
    
//     // Read directory and filter for PDF files
//     const files = await fs.readdir(processedDir);
//     const pdfFiles = files.filter((file) => file.toLowerCase().endsWith(".pdf"));

//     return NextResponse.json({ files: pdfFiles });
//   } catch (error) {
//     return NextResponse.json(
//       { error: "Failed to load PDF files" },
//       { status: 500 }
//     );
//   }
// }
