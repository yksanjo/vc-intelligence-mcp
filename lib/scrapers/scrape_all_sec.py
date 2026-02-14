#!/usr/bin/env python3
"""
Scrape ALL investment-related entities from SEC
Target: 10,000+ investors
"""

import requests
import time
import os
import json
import re
import pandas as pd
from datetime import datetime

class SECMegaScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'VC Intelligence Research contact@example.com',
            'Accept': 'application/json',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_all_companies(self):
        """Get ALL companies from SEC"""
        print("📡 Fetching ALL SEC registered companies...")

        url = "https://www.sec.gov/files/company_tickers.json"
        response = self.session.get(url, timeout=60)
        data = response.json()

        companies = []
        for key, company in data.items():
            companies.append({
                'cik': str(company['cik_str']),
                'name': company['title'],
                'ticker': company.get('ticker', '')
            })

        print(f"✅ Total SEC companies: {len(companies)}")
        return companies

    def filter_investment_companies(self, companies):
        """Filter to investment-related companies using broad keywords"""

        # Very broad keywords to catch all investment entities
        keywords = [
            # Core investment terms
            'capital', 'venture', 'partners', 'investment', 'fund', 'funds',
            'equity', 'management', 'advisors', 'advisory', 'holdings',
            'asset', 'wealth', 'trust', 'financial', 'securities',
            'hedge', 'private', 'growth', 'credit', 'income',

            # Fund types
            'etf', 'reit', 'mutual', 'closed-end', 'money market',
            'dividend', 'bond', 'fixed income', 'floating',

            # Structures
            'lp', 'llc', 'corp', 'inc', 'limited', 'partnership',

            # More specific
            'acquisition', 'spac', 'blank check', 'merger',
            'opportunities', 'strategic', 'global', 'international',

            # Family office indicators
            'family', 'office', 'estate', 'foundation',
        ]

        filtered = []
        for company in companies:
            name_lower = company['name'].lower()
            if any(kw in name_lower for kw in keywords):
                filtered.append(company)

        print(f"✅ Investment-related: {len(filtered)}")
        return filtered

    def enrich_batch(self, companies, batch_size=100, max_enrich=2000):
        """Enrich company data in batches"""
        print(f"📡 Enriching {min(max_enrich, len(companies))} companies...")

        enriched = []

        for i, company in enumerate(companies[:max_enrich]):
            if i % 100 == 0:
                print(f"   Progress: {i}/{min(max_enrich, len(companies))}")

            # Get details from SEC API
            cik_padded = company['cik'].zfill(10)
            url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"

            try:
                response = self.session.get(url, timeout=10)
                time.sleep(0.1)  # Rate limiting

                if response.status_code == 200:
                    data = response.json()
                    addresses = data.get('addresses', {})
                    business = addresses.get('business', {})

                    company['address'] = f"{business.get('street1', '')} {business.get('city', '')}, {business.get('stateOrCountry', '')}".strip()
                    company['city'] = business.get('city', '')
                    company['state'] = business.get('stateOrCountry', '')
                    company['phone'] = data.get('phone', '')
                    company['sic'] = data.get('sic', '')
                    company['sic_description'] = data.get('sicDescription', '')

            except:
                pass

            enriched.append(company)

        # Add remaining without enrichment
        for company in companies[max_enrich:]:
            enriched.append(company)

        return enriched

    def classify_type(self, name, sic_desc=''):
        """Classify investor type"""
        combined = f"{name.lower()} {sic_desc.lower() if sic_desc else ''}"

        if any(kw in combined for kw in ['family office', 'family investment', 'estate']):
            return 'Family Office'
        if any(kw in combined for kw in ['venture', 'ventures', 'seed', 'startup', 'early stage']):
            return 'Venture Capital'
        if any(kw in combined for kw in ['private equity', 'buyout', 'lbo', 'leveraged']):
            return 'Private Equity'
        if any(kw in combined for kw in ['hedge fund', 'hedge', 'alternative']):
            return 'Hedge Fund'
        if any(kw in combined for kw in ['etf', 'exchange traded']):
            return 'ETF'
        if any(kw in combined for kw in ['reit', 'real estate investment']):
            return 'REIT'
        if any(kw in combined for kw in ['mutual fund', 'open-end']):
            return 'Mutual Fund'
        if any(kw in combined for kw in ['closed-end', 'closed end']):
            return 'Closed-End Fund'
        if any(kw in combined for kw in ['trust']):
            return 'Trust'
        if any(kw in combined for kw in ['asset management', 'wealth management']):
            return 'Asset Management'
        if any(kw in combined for kw in ['capital', 'partners', 'fund', 'investment']):
            return 'Investment Company'

        return 'Other Institutional'


def main():
    print("=" * 70)
    print("🚀 SEC MEGA SCRAPER - ALL INVESTMENT ENTITIES")
    print("=" * 70)

    scraper = SECMegaScraper()

    # Get all companies
    all_companies = scraper.get_all_companies()

    # Filter to investment-related
    investment_cos = scraper.filter_investment_companies(all_companies)

    # Enrich with details
    enriched = scraper.enrich_batch(investment_cos, max_enrich=3000)

    # Classify
    for company in enriched:
        company['type'] = scraper.classify_type(
            company['name'],
            company.get('sic_description', '')
        )

        # Add focus flags
        combined = f"{company['name'].lower()} {company.get('sic_description', '').lower()}"
        company['has_ai_focus'] = any(t in combined for t in ['tech', 'software', 'ai', 'machine', 'data', 'cyber', 'cloud'])
        company['has_fintech_focus'] = any(t in combined for t in ['fintech', 'financial', 'bank', 'payment', 'credit', 'insurance'])
        company['has_music_focus'] = any(t in combined for t in ['music', 'entertainment', 'media', 'streaming', 'content'])

    # Save
    df = pd.DataFrame(enriched)

    print("\n" + "=" * 70)
    print("📈 RESULTS")
    print("=" * 70)
    print(f"\nTotal scraped: {len(df)}")
    print("\nBy Type:")
    print(df['type'].value_counts().head(15).to_string())

    output_file = os.path.join(os.path.dirname(__file__), 'vc_database_mega.csv')
    df.to_csv(output_file, index=False)
    print(f"\n💾 Saved: {output_file}")

    return df


if __name__ == "__main__":
    main()
