import { NextRequest, NextResponse } from "next/server";

// This endpoint triggers the scraper (calls Python backend or runs inline)
// For MVP, this is a placeholder that will connect to the Python scraper

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { type = "sec", limit = 100 } = body;

    // In production, this would:
    // 1. Trigger a background job (e.g., via Vercel Cron or external service)
    // 2. Call a Python microservice running the SEC scraper
    // 3. Queue the scraping job and return a job ID

    // For now, return a placeholder response
    return NextResponse.json({
      success: true,
      message: `Scraping job queued for ${type} with limit ${limit}`,
      job_id: `job_${Date.now()}`,
      status: "queued",
      estimated_time: "5-10 minutes",
      instructions: {
        note: "The scraper runs as a separate Python service",
        setup: [
          "1. Set up a Railway or Render deployment for the Python scraper",
          "2. Configure SCRAPER_API_URL environment variable",
          "3. The scraper will POST results to /api/investors/bulk",
        ],
        manual: "Run: python scripts/sec_scraper.py --limit 100",
      },
    });
  } catch (error) {
    console.error("Scrape API error:", error);
    return NextResponse.json(
      { error: "Failed to start scraping job" },
      { status: 500 }
    );
  }
}

export async function GET() {
  // Return scraping status/history
  return NextResponse.json({
    available_sources: [
      {
        id: "sec_adv",
        name: "SEC Form ADV",
        description: "Investment advisers with $150M+ AUM",
        estimated_records: "15,000+",
      },
      {
        id: "sec_13f",
        name: "SEC 13F Filings",
        description: "Institutional investors with $100M+ holdings",
        estimated_records: "10,000+",
      },
      {
        id: "crunchbase",
        name: "Crunchbase (requires API key)",
        description: "VC portfolio data and funding rounds",
        estimated_records: "50,000+",
      },
    ],
    last_scrape: null,
    next_scheduled: null,
  });
}
