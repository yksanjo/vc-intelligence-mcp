#!/usr/bin/env python3
"""
Upload investor data from CSV to Supabase
Run: python upload_to_supabase.py
"""

import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def get_supabase_client() -> Client:
    """Create Supabase client"""
    url = os.environ.get("SUPABASE_URL") or os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")

    if not url or not key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY environment variables")

    return create_client(url, key)


def parse_focus_flags(row: dict) -> dict:
    """Parse sector focus flags from sectors field"""
    sectors = str(row.get("sectors", "")).lower()
    investment_focus = str(row.get("investment_focus", "")).lower()
    combined = f"{sectors} {investment_focus}"

    return {
        "has_ai_focus": any(term in combined for term in ["ai", "ml", "machine learning", "artificial intelligence"]),
        "has_music_focus": "music" in combined or "entertainment" in combined,
        "has_fintech_focus": "fintech" in combined or "finance" in combined or "banking" in combined,
    }


def upload_csv_to_supabase(csv_path: str):
    """Upload CSV data to Supabase investors table"""
    print(f"Loading data from {csv_path}...")

    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} records")

    # Get Supabase client
    supabase = get_supabase_client()

    # Prepare records
    records = []
    for _, row in df.iterrows():
        record = {
            "cik": str(row.get("cik", "")) if pd.notna(row.get("cik")) else None,
            "name": row.get("name", ""),
            "type": row.get("type", ""),
            "address": row.get("address", "") if pd.notna(row.get("address")) else None,
            "city": row.get("city", "") if pd.notna(row.get("city")) else None,
            "state": row.get("state", "") if pd.notna(row.get("state")) else None,
            "aum_estimate": row.get("aum_estimate", "") if pd.notna(row.get("aum_estimate")) else None,
            "investment_focus": row.get("investment_focus", "") if pd.notna(row.get("investment_focus")) else None,
            "stage_preference": row.get("stage_preference", "") if pd.notna(row.get("stage_preference")) else None,
            "sectors": row.get("sectors", "") if pd.notna(row.get("sectors")) else None,
            "geography": row.get("geography", "") if pd.notna(row.get("geography")) else None,
            "website": row.get("website", "") if pd.notna(row.get("website")) else None,
            "contact_email": row.get("contact_email", "") if pd.notna(row.get("contact_email")) else None,
            "notable_investments": row.get("notable_investments", "") if pd.notna(row.get("notable_investments")) else None,
            "decision_makers": row.get("decision_makers", "") if pd.notna(row.get("decision_makers")) else None,
            "sec_url": row.get("sec_url", "") if pd.notna(row.get("sec_url")) else None,
        }

        # Add focus flags
        flags = parse_focus_flags(row.to_dict())
        record.update(flags)

        records.append(record)

    print(f"Uploading {len(records)} records to Supabase...")

    # Upload in batches of 100
    batch_size = 100
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        try:
            result = supabase.table("investors").upsert(batch, on_conflict="cik").execute()
            print(f"Uploaded batch {i // batch_size + 1}/{(len(records) + batch_size - 1) // batch_size}")
        except Exception as e:
            print(f"Error uploading batch: {e}")
            # Try inserting one by one to find problematic records
            for record in batch:
                try:
                    supabase.table("investors").insert(record).execute()
                except Exception as inner_e:
                    print(f"Failed to insert {record.get('name')}: {inner_e}")

    print("Upload complete!")


def main():
    import sys

    csv_path = sys.argv[1] if len(sys.argv) > 1 else "vc_database_sample.csv"

    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        print("Usage: python upload_to_supabase.py <csv_file>")
        sys.exit(1)

    upload_csv_to_supabase(csv_path)


if __name__ == "__main__":
    main()
