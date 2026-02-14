#!/usr/bin/env python3
"""
SEC EDGAR Full Scraper - 10,000+ Investors
Scrapes Form ADV, 13F, and Form D filings
"""

import requests
import json
import time
import re
import os
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd

class SECFullScraper:
    """Scrape all investment-related entities from SEC EDGAR"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'VC Intelligence Research contact@example.com',
            'Accept': 'application/json, text/html, application/xml',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.rate_limit_delay = 0.1  # SEC allows 10 requests/second

    def get_all_investment_companies(self) -> List[Dict]:
        """Get ALL companies from SEC with investment-related keywords"""
        print("📡 Fetching full company list from SEC...")

        url = "https://www.sec.gov/files/company_tickers.json"

        try:
            response = self.session.get(url, timeout=60)
            response.raise_for_status()
            data = response.json()

            investment_keywords = [
                'capital', 'venture', 'partners', 'investment', 'fund',
                'equity', 'management', 'advisors', 'advisory', 'holdings',
                'asset', 'wealth', 'family', 'trust', 'financial',
                'securities', 'hedge', 'private', 'growth', 'opportunities'
            ]

            companies = []
            for key, company in data.items():
                name_lower = company['title'].lower()
                if any(kw in name_lower for kw in investment_keywords):
                    companies.append({
                        'cik': str(company['cik_str']),
                        'name': company['title'],
                        'ticker': company.get('ticker', ''),
                        'source': 'sec_tickers'
                    })

            print(f"✅ Found {len(companies)} investment-related companies")
            return companies

        except Exception as e:
            print(f"❌ Error: {e}")
            return []

    def get_form_adv_filers(self, limit: int = 5000) -> List[Dict]:
        """
        Get Form ADV filers - Investment Advisers
        These are registered investment advisers with $150M+ AUM
        """
        print(f"📡 Fetching Form ADV filers (Investment Advisers)...")

        # SEC IAPD (Investment Adviser Public Disclosure) data
        # This is a comprehensive list of registered investment advisers

        advisers = []

        # Method 1: Use SEC's full-text search for ADV filers
        # The SEC EDGAR full-text search can find recent ADV filings

        base_url = "https://efts.sec.gov/LATEST/search-index"

        # Search for recent Form ADV filings
        params = {
            'q': '"form ADV"',
            'dateRange': 'custom',
            'startdt': '2024-01-01',
            'enddt': '2026-12-31',
            'forms': 'ADV-E,ADV-H,ADV-NR,ADV-W',
            'from': 0,
            'size': 100
        }

        print("   Searching via EDGAR full-text search...")

        # Alternative: Parse the IAPD bulk data
        # SEC provides bulk data files we can parse

        try:
            # Get recent filings feed
            feed_url = "https://www.sec.gov/cgi-bin/browse-edgar"

            for form_type in ['ADV', 'ADV-E']:
                params = {
                    'action': 'getcurrent',
                    'type': form_type,
                    'company': '',
                    'dateb': '',
                    'owner': 'include',
                    'count': 100,
                    'output': 'atom'
                }

                response = self.session.get(feed_url, params=params, timeout=30)
                time.sleep(self.rate_limit_delay)

                if response.status_code == 200:
                    content = response.text
                    entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)

                    for entry in entries:
                        name_match = re.search(r'<title[^>]*>([^<]+)</title>', entry)
                        cik_match = re.search(r'CIK=(\d+)', entry)

                        if name_match and cik_match:
                            name = re.sub(r'\s*\(.*?\)\s*$', '', name_match.group(1)).strip()
                            advisers.append({
                                'cik': cik_match.group(1),
                                'name': name,
                                'source': 'form_adv',
                                'filing_type': form_type
                            })

            print(f"✅ Found {len(advisers)} Form ADV filers")

        except Exception as e:
            print(f"❌ Error fetching Form ADV: {e}")

        return advisers

    def get_13f_filers(self, limit: int = 5000) -> List[Dict]:
        """
        Get 13F filers - Institutional Investment Managers
        These manage $100M+ in securities
        """
        print(f"📡 Fetching 13F filers (Institutional Investors)...")

        holders = []

        try:
            # Get the 13F securities list which also has filer info
            # Plus search recent 13F filings

            feed_url = "https://www.sec.gov/cgi-bin/browse-edgar"
            params = {
                'action': 'getcurrent',
                'type': '13F-HR',
                'company': '',
                'dateb': '',
                'owner': 'include',
                'count': 100,
                'output': 'atom'
            }

            response = self.session.get(feed_url, params=params, timeout=30)
            time.sleep(self.rate_limit_delay)

            if response.status_code == 200:
                content = response.text
                entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)

                for entry in entries:
                    name_match = re.search(r'<title[^>]*>([^<]+)</title>', entry)
                    cik_match = re.search(r'CIK=(\d+)', entry)

                    if name_match and cik_match:
                        name = re.sub(r'\s*\(13F.*?\)\s*$', '', name_match.group(1)).strip()
                        name = re.sub(r'\s*13F-HR.*$', '', name).strip()

                        holders.append({
                            'cik': cik_match.group(1),
                            'name': name,
                            'source': '13f_filing',
                            'filing_type': '13F-HR'
                        })

            print(f"✅ Found {len(holders)} 13F filers")

        except Exception as e:
            print(f"❌ Error fetching 13F: {e}")

        return holders

    def get_form_d_filers(self, limit: int = 5000) -> List[Dict]:
        """
        Get Form D filers - Private Fund Offerings
        These are private funds raising capital (VCs, PE, Hedge Funds)
        """
        print(f"📡 Fetching Form D filers (Private Funds)...")

        filers = []

        try:
            feed_url = "https://www.sec.gov/cgi-bin/browse-edgar"
            params = {
                'action': 'getcurrent',
                'type': 'D',
                'company': '',
                'dateb': '',
                'owner': 'include',
                'count': 100,
                'output': 'atom'
            }

            response = self.session.get(feed_url, params=params, timeout=30)
            time.sleep(self.rate_limit_delay)

            if response.status_code == 200:
                content = response.text
                entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)

                for entry in entries:
                    name_match = re.search(r'<title[^>]*>([^<]+)</title>', entry)
                    cik_match = re.search(r'CIK=(\d+)', entry)

                    if name_match and cik_match:
                        name = re.sub(r'\s*\(D\)\s*$', '', name_match.group(1)).strip()

                        filers.append({
                            'cik': cik_match.group(1),
                            'name': name,
                            'source': 'form_d',
                            'filing_type': 'D'
                        })

            print(f"✅ Found {len(filers)} Form D filers")

        except Exception as e:
            print(f"❌ Error fetching Form D: {e}")

        return filers

    def get_company_details(self, cik: str) -> Optional[Dict]:
        """Get detailed company info from SEC submissions API"""
        cik_padded = cik.zfill(10)
        url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"

        try:
            response = self.session.get(url, timeout=15)
            time.sleep(self.rate_limit_delay)

            if response.status_code == 200:
                data = response.json()
                addresses = data.get('addresses', {})
                business = addresses.get('business', {})

                return {
                    'address': f"{business.get('street1', '')} {business.get('street2', '')}, {business.get('city', '')}, {business.get('stateOrCountry', '')} {business.get('zipCode', '')}".strip().strip(','),
                    'city': business.get('city', ''),
                    'state': business.get('stateOrCountry', ''),
                    'phone': data.get('phone', ''),
                    'sic': data.get('sic', ''),
                    'sic_description': data.get('sicDescription', ''),
                    'fiscal_year_end': data.get('fiscalYearEnd', ''),
                }
        except:
            pass

        return None

    def classify_investor_type(self, name: str, sic_desc: str = '', source: str = '') -> str:
        """Classify investor type based on name, SIC, and source"""
        name_lower = name.lower()
        combined = f"{name_lower} {sic_desc.lower() if sic_desc else ''}"

        # Source-based classification
        if source == 'form_d':
            if 'venture' in combined:
                return 'Venture Capital'
            elif 'private equity' in combined or 'buyout' in combined:
                return 'Private Equity'
            elif 'hedge' in combined:
                return 'Hedge Fund'
            return 'Private Fund'

        if source == '13f_filing':
            return 'Institutional Investor'

        if source == 'form_adv':
            return 'Investment Adviser'

        # Name-based classification
        if any(kw in combined for kw in ['family office', 'family investment']):
            return 'Family Office'
        if any(kw in combined for kw in ['venture', 'ventures', 'seed', 'startup']):
            return 'Venture Capital'
        if any(kw in combined for kw in ['private equity', 'buyout', 'lbo']):
            return 'Private Equity'
        if any(kw in combined for kw in ['hedge fund', 'hedge']):
            return 'Hedge Fund'
        if any(kw in combined for kw in ['trust', 'estate']):
            return 'Family Office'
        if any(kw in combined for kw in ['asset management', 'wealth management']):
            return 'Asset Management'
        if any(kw in combined for kw in ['capital', 'partners', 'fund', 'investment']):
            return 'Investment Company'

        return 'Other Institutional'


def main():
    """Main scraping function"""
    print("=" * 70)
    print("🚀 SEC EDGAR FULL SCRAPER - 10,000+ INVESTORS")
    print("=" * 70)
    print()

    scraper = SECFullScraper()
    all_investors = []
    seen_ciks = set()

    # Phase 1: Company tickers (investment-related)
    print("\n" + "=" * 70)
    print("📊 PHASE 1: Investment Companies from SEC Registry")
    print("=" * 70)
    companies = scraper.get_all_investment_companies()

    for company in companies:
        if company['cik'] not in seen_ciks:
            seen_ciks.add(company['cik'])
            all_investors.append(company)

    print(f"   Added {len(companies)} companies (Total: {len(all_investors)})")

    # Phase 2: Form ADV filers
    print("\n" + "=" * 70)
    print("📊 PHASE 2: Form ADV Investment Advisers")
    print("=" * 70)
    advisers = scraper.get_form_adv_filers()

    added = 0
    for adviser in advisers:
        if adviser['cik'] not in seen_ciks:
            seen_ciks.add(adviser['cik'])
            all_investors.append(adviser)
            added += 1

    print(f"   Added {added} new advisers (Total: {len(all_investors)})")

    # Phase 3: 13F filers
    print("\n" + "=" * 70)
    print("📊 PHASE 3: 13F Institutional Investors")
    print("=" * 70)
    holders = scraper.get_13f_filers()

    added = 0
    for holder in holders:
        if holder['cik'] not in seen_ciks:
            seen_ciks.add(holder['cik'])
            all_investors.append(holder)
            added += 1

    print(f"   Added {added} new 13F filers (Total: {len(all_investors)})")

    # Phase 4: Form D filers
    print("\n" + "=" * 70)
    print("📊 PHASE 4: Form D Private Funds")
    print("=" * 70)
    form_d = scraper.get_form_d_filers()

    added = 0
    for filer in form_d:
        if filer['cik'] not in seen_ciks:
            seen_ciks.add(filer['cik'])
            all_investors.append(filer)
            added += 1

    print(f"   Added {added} new Form D filers (Total: {len(all_investors)})")

    # Phase 5: Enrich with details (sample for speed)
    print("\n" + "=" * 70)
    print("📊 PHASE 5: Enriching Data (first 500)")
    print("=" * 70)

    enrich_limit = min(500, len(all_investors))
    for i, investor in enumerate(all_investors[:enrich_limit]):
        if i % 50 == 0:
            print(f"   Processing {i+1}/{enrich_limit}...")

        details = scraper.get_company_details(investor['cik'])
        if details:
            investor.update(details)

        investor['type'] = scraper.classify_investor_type(
            investor['name'],
            investor.get('sic_description', ''),
            investor.get('source', '')
        )

    # Classify remaining without API calls
    for investor in all_investors[enrich_limit:]:
        investor['type'] = scraper.classify_investor_type(
            investor['name'],
            '',
            investor.get('source', '')
        )

    # Create DataFrame
    df = pd.DataFrame(all_investors)

    # Summary
    print("\n" + "=" * 70)
    print("📈 FINAL RESULTS")
    print("=" * 70)
    print(f"\nTotal investors scraped: {len(df)}")
    print("\nBy Type:")
    if 'type' in df.columns:
        print(df['type'].value_counts().to_string())
    print("\nBy Source:")
    if 'source' in df.columns:
        print(df['source'].value_counts().to_string())

    # Save
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'vc_database_full.csv')
    df.to_csv(output_file, index=False)
    print(f"\n💾 Saved to: {output_file}")

    return df


if __name__ == "__main__":
    df = main()

    print("\n" + "=" * 70)
    print("📋 TO GET 10,000+ INVESTORS:")
    print("=" * 70)
    print("""
1. SEC IAPD Bulk Data (FREE - 15,000+ advisers):
   Download from: https://www.sec.gov/help/foiadocsinvaaborslst

2. Crunchbase API ($49-299/mo - 50,000+ investors):
   Sign up at: https://data.crunchbase.com/

3. OpenCorporates API (FREE tier available):
   https://opencorporates.com/

4. Run this scraper multiple times with different date ranges
   to accumulate more Form D/ADV/13F filings over time.
""")
