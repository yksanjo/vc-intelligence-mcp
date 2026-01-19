#!/usr/bin/env python3
"""
SEC EDGAR Form ADV Scraper
Extracts family office and VC firm data from SEC filings
"""

import requests
import json
import time
import re
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd

class SECFormADVScraper:
    """Scrape investment adviser data from SEC EDGAR"""
    
    def __init__(self):
        self.base_url = "https://www.sec.gov"
        self.headers = {
            'User-Agent': 'VC Intelligence Research yoshi@soundraw.io',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.sec.gov'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def search_advisers(self, state: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """
        Search for investment advisers using SEC EDGAR
        
        Args:
            state: Two-letter state code (e.g., 'NY', 'CA') or None for all
            limit: Maximum number of results to retrieve
            
        Returns:
            List of adviser data dictionaries
        """
        print(f"🔍 Searching SEC EDGAR for investment advisers...")
        
        # SEC's Company Search API endpoint
        search_url = f"{self.base_url}/cgi-bin/browse-edgar"
        
        advisers = []
        
        # Search for Form ADV filers
        # We'll use the browse endpoint to get companies that filed Form ADV
        params = {
            'action': 'getcompany',
            'type': 'ADV',
            'count': limit,
            'output': 'atom'
        }
        
        if state:
            params['State'] = state
            
        try:
            print(f"📡 Fetching data from SEC EDGAR...")
            response = self.session.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse the response
            # Note: SEC returns Atom XML feed, we'll extract company info
            content = response.text
            
            # Extract CIK numbers and company names from the feed
            cik_pattern = r'<cik>(\d+)</cik>'
            name_pattern = r'<title>(.+?)</title>'
            
            ciks = re.findall(cik_pattern, content)
            names = re.findall(name_pattern, content)
            
            # Filter out feed metadata titles
            company_names = [n for n in names if 'SEC' not in n and 'EDGAR' not in n]
            
            print(f"✅ Found {len(ciks)} potential investment advisers")
            
            # Get detailed data for each adviser
            for i, (cik, name) in enumerate(zip(ciks[:limit], company_names[:limit])):
                if i % 10 == 0:
                    print(f"   Processing {i+1}/{min(limit, len(ciks))}...")
                    time.sleep(0.1)  # Rate limiting - be nice to SEC servers
                
                adviser_data = self.get_adviser_details(cik, name)
                if adviser_data:
                    advisers.append(adviser_data)
                    
        except Exception as e:
            print(f"❌ Error searching advisers: {e}")
            
        return advisers
    
    def get_adviser_details(self, cik: str, name: str) -> Optional[Dict]:
        """
        Get detailed information about an investment adviser
        
        Args:
            cik: Central Index Key (SEC identifier)
            name: Company name
            
        Returns:
            Dictionary with adviser details or None
        """
        # Pad CIK to 10 digits
        cik_padded = cik.zfill(10)
        
        # Try to get submissions data
        submissions_url = f"{self.base_url}/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=ADV&dateb=&owner=exclude&count=1"
        
        try:
            response = self.session.get(submissions_url, timeout=15)
            
            if response.status_code == 200:
                # Extract basic info from the page
                content = response.text
                
                # Try to find business address
                address_match = re.search(r'<div class="mailer">(.*?)</div>', content, re.DOTALL)
                address = ""
                if address_match:
                    address_text = address_match.group(1)
                    address = re.sub(r'<[^>]+>', ' ', address_text).strip()
                    address = ' '.join(address.split())
                
                return {
                    'cik': cik,
                    'name': name.strip(),
                    'address': address,
                    'sec_url': f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=ADV",
                    'scraped_at': datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"⚠️  Error getting details for {name}: {e}")
            
        return None
    
    def get_form_13f_holders(self, limit: int = 100) -> List[Dict]:
        """
        Get institutional investors from 13F filings
        These are investors managing $100M+ in securities
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of institutional investor data
        """
        print(f"🔍 Searching for 13F institutional investors...")
        
        search_url = f"{self.base_url}/cgi-bin/browse-edgar"
        params = {
            'action': 'getcompany',
            'type': '13F-HR',
            'count': limit,
            'output': 'atom'
        }
        
        holders = []
        
        try:
            response = self.session.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            content = response.text
            
            # Extract data
            cik_pattern = r'<cik>(\d+)</cik>'
            name_pattern = r'<title>(.+?)</title>'
            
            ciks = re.findall(cik_pattern, content)
            names = re.findall(name_pattern, content)
            
            company_names = [n for n in names if 'SEC' not in n and 'EDGAR' not in n]
            
            print(f"✅ Found {len(ciks)} institutional investors with 13F filings")
            
            for i, (cik, name) in enumerate(zip(ciks[:limit], company_names[:limit])):
                if i % 10 == 0:
                    print(f"   Processing {i+1}/{min(limit, len(ciks))}...")
                    time.sleep(0.1)
                
                holders.append({
                    'cik': cik,
                    'name': name.strip(),
                    'filing_type': '13F-HR',
                    'sec_url': f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=13F-HR",
                    'scraped_at': datetime.now().isoformat()
                })
                
        except Exception as e:
            print(f"❌ Error searching 13F holders: {e}")
            
        return holders
    
    def classify_investor_type(self, name: str) -> str:
        """
        Classify investor based on name patterns
        
        Args:
            name: Company/fund name
            
        Returns:
            Investor type classification
        """
        name_lower = name.lower()
        
        # Family office indicators
        family_keywords = ['family', 'office', 'investment co', 'holdings', 'trust']
        if any(kw in name_lower for kw in family_keywords):
            return 'Family Office'
        
        # VC indicators
        vc_keywords = ['venture', 'ventures', 'capital', 'partners', 'fund']
        if any(kw in name_lower for kw in vc_keywords):
            return 'Venture Capital'
        
        # PE indicators
        pe_keywords = ['equity', 'private equity', 'investment']
        if any(kw in name_lower for kw in pe_keywords):
            return 'Private Equity'
        
        # Hedge fund indicators
        hf_keywords = ['hedge', 'offshore', 'fund', 'asset management']
        if any(kw in name_lower for kw in hf_keywords):
            return 'Hedge Fund'
        
        return 'Other Institutional'

def main():
    """Main execution function"""
    print("=" * 60)
    print("🚀 SEC EDGAR INVESTMENT INTELLIGENCE SCRAPER")
    print("=" * 60)
    print()
    
    scraper = SECFormADVScraper()
    
    # Collect data
    all_investors = []
    
    # Get Form ADV filers (investment advisers)
    print("\n📊 Phase 1: Form ADV Investment Advisers")
    print("-" * 60)
    advisers = scraper.search_advisers(limit=50)
    all_investors.extend(advisers)
    
    # Get 13F holders (institutional investors)
    print("\n📊 Phase 2: 13F Institutional Holders")
    print("-" * 60)
    holders = scraper.get_form_13f_holders(limit=50)
    all_investors.extend(holders)
    
    # Classify investors
    print("\n🏷️  Classifying investors...")
    for investor in all_investors:
        investor['type'] = scraper.classify_investor_type(investor['name'])
    
    # Create DataFrame
    df = pd.DataFrame(all_investors)
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("📈 RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total investors found: {len(df)}")
    print("\nBreakdown by type:")
    if 'type' in df.columns:
        print(df['type'].value_counts().to_string())
    
    # Save to CSV
    output_file = '/home/claude/vc_database.csv'
    df.to_csv(output_file, index=False)
    print(f"\n💾 Data saved to: {output_file}")
    
    # Show sample records
    print("\n📋 Sample Records:")
    print("-" * 60)
    print(df.head(10).to_string(index=False))
    
    return df

if __name__ == "__main__":
    df = main()
