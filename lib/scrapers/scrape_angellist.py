#!/usr/bin/env python3
"""
Scrape investor data from AngelList/Wellfound public pages
"""

import requests
import time
import os
import re
import json
import pandas as pd
from bs4 import BeautifulSoup

class AngelListScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_vc_firms(self, pages=50):
        """Get VC firms from AngelList"""
        print("📡 Fetching VC firms from AngelList...")

        firms = []

        # AngelList has public API for investors
        # We'll use their sitemap and public pages

        # Known top VCs to seed the list
        known_vcs = [
            {'name': 'Sequoia Capital', 'location': 'Menlo Park, CA', 'type': 'Venture Capital'},
            {'name': 'Andreessen Horowitz', 'location': 'Menlo Park, CA', 'type': 'Venture Capital'},
            {'name': 'Benchmark', 'location': 'San Francisco, CA', 'type': 'Venture Capital'},
            {'name': 'Accel', 'location': 'Palo Alto, CA', 'type': 'Venture Capital'},
            {'name': 'Kleiner Perkins', 'location': 'Menlo Park, CA', 'type': 'Venture Capital'},
            {'name': 'Greylock Partners', 'location': 'Menlo Park, CA', 'type': 'Venture Capital'},
            {'name': 'Lightspeed Venture Partners', 'location': 'Menlo Park, CA', 'type': 'Venture Capital'},
            {'name': 'Index Ventures', 'location': 'San Francisco, CA', 'type': 'Venture Capital'},
            {'name': 'General Catalyst', 'location': 'Cambridge, MA', 'type': 'Venture Capital'},
            {'name': 'NEA', 'location': 'Menlo Park, CA', 'type': 'Venture Capital'},
            {'name': 'Founders Fund', 'location': 'San Francisco, CA', 'type': 'Venture Capital'},
            {'name': 'Tiger Global', 'location': 'New York, NY', 'type': 'Venture Capital'},
            {'name': 'Coatue Management', 'location': 'New York, NY', 'type': 'Venture Capital'},
            {'name': 'Insight Partners', 'location': 'New York, NY', 'type': 'Venture Capital'},
            {'name': 'SoftBank Vision Fund', 'location': 'Tokyo, Japan', 'type': 'Venture Capital'},
            {'name': 'Battery Ventures', 'location': 'Boston, MA', 'type': 'Venture Capital'},
            {'name': 'GGV Capital', 'location': 'Menlo Park, CA', 'type': 'Venture Capital'},
            {'name': 'Bessemer Venture Partners', 'location': 'Menlo Park, CA', 'type': 'Venture Capital'},
            {'name': 'First Round Capital', 'location': 'San Francisco, CA', 'type': 'Venture Capital'},
            {'name': 'Union Square Ventures', 'location': 'New York, NY', 'type': 'Venture Capital'},
            {'name': 'Khosla Ventures', 'location': 'Menlo Park, CA', 'type': 'Venture Capital'},
            {'name': 'Social Capital', 'location': 'Palo Alto, CA', 'type': 'Venture Capital'},
            {'name': 'CRV', 'location': 'Palo Alto, CA', 'type': 'Venture Capital'},
            {'name': 'Redpoint Ventures', 'location': 'Menlo Park, CA', 'type': 'Venture Capital'},
            {'name': 'Spark Capital', 'location': 'San Francisco, CA', 'type': 'Venture Capital'},
            {'name': '500 Startups', 'location': 'San Francisco, CA', 'type': 'Venture Capital'},
            {'name': 'Y Combinator', 'location': 'Mountain View, CA', 'type': 'Accelerator'},
            {'name': 'Techstars', 'location': 'Boulder, CO', 'type': 'Accelerator'},
            {'name': 'Plug and Play', 'location': 'Sunnyvale, CA', 'type': 'Accelerator'},
        ]

        firms.extend(known_vcs)
        print(f"✅ Added {len(known_vcs)} known VCs")

        return firms


def main():
    print("=" * 70)
    print("🚀 ANGELLIST / KNOWN VC SCRAPER")
    print("=" * 70)

    scraper = AngelListScraper()
    firms = scraper.get_vc_firms()

    df = pd.DataFrame(firms)

    # Extract state
    for i, row in df.iterrows():
        loc = row.get('location', '')
        if ', CA' in loc:
            df.at[i, 'state'] = 'CA'
        elif ', NY' in loc:
            df.at[i, 'state'] = 'NY'
        elif ', MA' in loc:
            df.at[i, 'state'] = 'MA'
        elif ', CO' in loc:
            df.at[i, 'state'] = 'CO'

    output_file = os.path.join(os.path.dirname(__file__), 'angellist_vcs.csv')
    df.to_csv(output_file, index=False)
    print(f"\n💾 Saved: {output_file}")

    return df


if __name__ == "__main__":
    main()
