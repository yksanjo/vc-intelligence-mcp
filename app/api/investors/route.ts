import { NextRequest, NextResponse } from "next/server";
import { createClient } from "@/lib/supabase/server";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const type = searchParams.get("type");
    const state = searchParams.get("state");
    const has_ai_focus = searchParams.get("has_ai_focus") === "true";
    const has_fintech_focus = searchParams.get("has_fintech_focus") === "true";
    const has_music_focus = searchParams.get("has_music_focus") === "true";
    const search = searchParams.get("search");
    const limit = parseInt(searchParams.get("limit") || "100");
    const offset = parseInt(searchParams.get("offset") || "0");

    const supabase = await createClient();

    let query = supabase.from("investors").select("*");

    if (type) {
      query = query.eq("type", type);
    }

    if (state) {
      query = query.eq("state", state);
    }

    if (has_ai_focus) {
      query = query.eq("has_ai_focus", true);
    }

    if (has_fintech_focus) {
      query = query.eq("has_fintech_focus", true);
    }

    if (has_music_focus) {
      query = query.eq("has_music_focus", true);
    }

    if (search) {
      query = query.or(
        `name.ilike.%${search}%,sectors.ilike.%${search}%,investment_focus.ilike.%${search}%`
      );
    }

    const { data, error, count } = await query
      .order("name")
      .range(offset, offset + limit - 1);

    if (error) {
      console.error("Supabase error:", error);
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({
      investors: data || [],
      total: count || data?.length || 0,
      limit,
      offset,
    });
  } catch (error) {
    console.error("API error:", error);
    return NextResponse.json(
      { error: "Failed to fetch investors" },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const supabase = await createClient();

    const { data, error } = await supabase
      .from("investors")
      .insert(body)
      .select()
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ investor: data }, { status: 201 });
  } catch (error) {
    console.error("API error:", error);
    return NextResponse.json(
      { error: "Failed to create investor" },
      { status: 500 }
    );
  }
}
