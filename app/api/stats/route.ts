import { NextResponse } from "next/server";
import { createClient } from "@/lib/supabase/server";

export async function GET() {
  try {
    const supabase = await createClient();

    // Get total count
    const { count: totalCount } = await supabase
      .from("investors")
      .select("*", { count: "exact", head: true });

    // Get counts by type
    const { data: typeData } = await supabase.from("investors").select("type");

    const byType: Record<string, number> = {};
    typeData?.forEach((row) => {
      if (row.type) {
        byType[row.type] = (byType[row.type] || 0) + 1;
      }
    });

    // Get AI-focused count
    const { count: aiCount } = await supabase
      .from("investors")
      .select("*", { count: "exact", head: true })
      .eq("has_ai_focus", true);

    // Get Fintech-focused count
    const { count: fintechCount } = await supabase
      .from("investors")
      .select("*", { count: "exact", head: true })
      .eq("has_fintech_focus", true);

    // Get Music-focused count
    const { count: musicCount } = await supabase
      .from("investors")
      .select("*", { count: "exact", head: true })
      .eq("has_music_focus", true);

    // Get top states
    const { data: stateData } = await supabase.from("investors").select("state");

    const topStates: Record<string, number> = {};
    stateData?.forEach((row) => {
      if (row.state) {
        topStates[row.state] = (topStates[row.state] || 0) + 1;
      }
    });

    // Sort states by count
    const sortedStates = Object.entries(topStates)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .reduce((acc, [state, count]) => {
        acc[state] = count;
        return acc;
      }, {} as Record<string, number>);

    // Get the most recent scraped_at timestamp for data freshness
    const { data: recentData } = await supabase
      .from("investors")
      .select("scraped_at")
      .not("scraped_at", "is", null)
      .order("scraped_at", { ascending: false })
      .limit(1);

    const lastUpdated = recentData && recentData.length > 0 
      ? recentData[0].scraped_at 
      : null;

    // Calculate data freshness status
    let freshnessStatus = "unknown";
    if (lastUpdated) {
      const lastUpdateDate = new Date(lastUpdated);
      const now = new Date();
      const diffHours = (now.getTime() - lastUpdateDate.getTime()) / (1000 * 60 * 60);
      
      if (diffHours <= 24) {
        freshnessStatus = "live";
      } else if (diffHours <= 168) { // 7 days
        freshnessStatus = "recent";
      } else {
        freshnessStatus = "stale";
      }
    }

    return NextResponse.json({
      total_investors: totalCount || 0,
      by_type: byType,
      top_states: sortedStates,
      ai_investors: aiCount || 0,
      fintech_investors: fintechCount || 0,
      music_investors: musicCount || 0,
      last_updated: lastUpdated,
      freshness_status: freshnessStatus,
    });
  } catch (error) {
    console.error("Stats API error:", error);
    return NextResponse.json(
      { error: "Failed to fetch stats" },
      { status: 500 }
    );
  }
}
