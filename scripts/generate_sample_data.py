#!/usr/bin/env python3
"""
Generate sample VC and family office data
This demonstrates the data structure for when you run the real scraper
"""

import pandas as pd
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate realistic sample investor data"""
    
    # Sample family offices
    family_offices = [
        {
            'cik': '0001234567',
            'name': 'Rockefeller Capital Management',
            'type': 'Family Office',
            'address': '10 Rockefeller Plaza, New York, NY 10020',
            'aum_estimate': '10B+',
            'investment_focus': 'Multi-strategy, Global Markets',
            'stage_preference': 'Growth, Late Stage',
            'sectors': 'Technology, Healthcare, Real Estate',
            'geography': 'Global',
            'website': 'rockcap.com',
            'contact_email': 'info@rockcap.com',
            'sec_url': 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001234567',
            'notable_investments': 'Multiple tech unicorns',
            'decision_makers': 'Greg Fleming (CEO)',
            'scraped_at': datetime.now().isoformat()
        },
        {
            'cik': '0001234568',
            'name': 'Bessemer Trust Company',
            'type': 'Family Office',
            'address': '630 Fifth Avenue, New York, NY 10111',
            'aum_estimate': '150B+',
            'investment_focus': 'Wealth Management, Private Investments',
            'stage_preference': 'Series A, Series B, Growth',
            'sectors': 'Fintech, AI/ML, Enterprise Software',
            'geography': 'North America, Europe',
            'website': 'bessemer.com',
            'contact_email': 'inquiries@bessemer.com',
            'sec_url': 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001234568',
            'notable_investments': 'Multiple fintech startups',
            'decision_makers': 'David Tyree (CIO)',
            'scraped_at': datetime.now().isoformat()
        },
        {
            'cik': '0001234569',
            'name': 'Iconiq Capital',
            'type': 'Family Office / VC Hybrid',
            'address': '394 Pacific Avenue, San Francisco, CA 94111',
            'aum_estimate': '50B+',
            'investment_focus': 'Technology, Growth Equity',
            'stage_preference': 'Series B, Series C, Growth',
            'sectors': 'Consumer Tech, SaaS, AI, Fintech',
            'geography': 'Global, Silicon Valley Focus',
            'website': 'iconiqcapital.com',
            'contact_email': 'investments@iconiqcapital.com',
            'sec_url': 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001234569',
            'notable_investments': 'Facebook, Twitter, Uber, Spotify',
            'decision_makers': 'Divesh Makan (Founder)',
            'scraped_at': datetime.now().isoformat()
        },
        {
            'cik': '0001234570',
            'name': 'Emerson Collective',
            'type': 'Family Office',
            'address': 'Palo Alto, CA',
            'aum_estimate': '15B+',
            'investment_focus': 'Social Impact, Technology',
            'stage_preference': 'Seed, Series A, Growth',
            'sectors': 'Education Tech, Climate, Immigration, Healthcare',
            'geography': 'United States',
            'website': 'emersoncollective.com',
            'contact_email': 'info@emersoncollective.com',
            'sec_url': 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001234570',
            'notable_investments': 'Multiple education startups',
            'decision_makers': 'Laurene Powell Jobs (Founder)',
            'scraped_at': datetime.now().isoformat()
        }
    ]
    
    # Sample VC firms
    vc_firms = [
        {
            'cik': '0001234571',
            'name': 'Andreessen Horowitz',
            'type': 'Venture Capital',
            'address': '2865 Sand Hill Road, Menlo Park, CA 94025',
            'aum_estimate': '35B+',
            'investment_focus': 'Technology, Crypto, Bio',
            'stage_preference': 'Seed to Growth',
            'sectors': 'AI/ML, Crypto, SaaS, Consumer, Bio',
            'geography': 'Global',
            'website': 'a16z.com',
            'contact_email': 'investments@a16z.com',
            'sec_url': 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001234571',
            'notable_investments': 'Airbnb, Coinbase, Facebook, GitHub, Slack',
            'decision_makers': 'Marc Andreessen, Ben Horowitz',
            'scraped_at': datetime.now().isoformat()
        },
        {
            'cik': '0001234572',
            'name': 'Sequoia Capital',
            'type': 'Venture Capital',
            'address': '2800 Sand Hill Road, Menlo Park, CA 94025',
            'aum_estimate': '85B+',
            'investment_focus': 'Technology, Global Markets',
            'stage_preference': 'Seed to Late Stage',
            'sectors': 'Enterprise, Consumer, Healthcare, Fintech, Crypto',
            'geography': 'Global (US, China, India, Europe)',
            'website': 'sequoiacap.com',
            'contact_email': 'info@sequoiacap.com',
            'sec_url': 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001234572',
            'notable_investments': 'Apple, Google, LinkedIn, Stripe, WhatsApp',
            'decision_makers': 'Roelof Botha, Doug Leone',
            'scraped_at': datetime.now().isoformat()
        },
        {
            'cik': '0001234573',
            'name': 'Benchmark Capital',
            'type': 'Venture Capital',
            'address': '2965 Woodside Road, Woodside, CA 94062',
            'aum_estimate': '10B+',
            'investment_focus': 'Early Stage Technology',
            'stage_preference': 'Seed, Series A',
            'sectors': 'Consumer, Enterprise Software, Mobile',
            'geography': 'United States',
            'website': 'benchmark.com',
            'contact_email': 'team@benchmark.com',
            'sec_url': 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001234573',
            'notable_investments': 'eBay, Twitter, Uber, Snapchat, Discord',
            'decision_makers': 'Bill Gurley, Sarah Tavel',
            'scraped_at': datetime.now().isoformat()
        },
        {
            'cik': '0001234574',
            'name': 'Lightspeed Venture Partners',
            'type': 'Venture Capital',
            'address': '2200 Sand Hill Road, Menlo Park, CA 94025',
            'aum_estimate': '18B+',
            'investment_focus': 'Enterprise & Consumer Technology',
            'stage_preference': 'Seed to Growth',
            'sectors': 'Enterprise SaaS, Fintech, Consumer, Health',
            'geography': 'Global (US, India, China, Europe)',
            'website': 'lsvp.com',
            'contact_email': 'info@lsvp.com',
            'sec_url': 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001234574',
            'notable_investments': 'Snap, Affirm, Epic Games, Nutanix',
            'decision_makers': 'Jeremy Liew, Nicole Quinn',
            'scraped_at': datetime.now().isoformat()
        }
    ]
    
    # Sample institutional investors (13F holders)
    institutional = [
        {
            'cik': '0001234575',
            'name': 'Vanguard Group Inc',
            'type': 'Institutional Investor',
            'address': 'Valley Forge, PA',
            'aum_estimate': '7T+',
            'investment_focus': 'Index Funds, ETFs',
            'stage_preference': 'Public Markets',
            'sectors': 'Diversified',
            'geography': 'Global',
            'website': 'vanguard.com',
            'contact_email': None,
            'sec_url': 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001234575',
            'notable_investments': 'Major positions in all large cap tech',
            'decision_makers': 'Mortimer J. Buckley (CEO)',
            'scraped_at': datetime.now().isoformat()
        },
        {
            'cik': '0001234576',
            'name': 'BlackRock Inc',
            'type': 'Institutional Investor',
            'address': 'New York, NY',
            'aum_estimate': '9T+',
            'investment_focus': 'Asset Management, Index Funds',
            'stage_preference': 'Public Markets',
            'sectors': 'Diversified',
            'geography': 'Global',
            'website': 'blackrock.com',
            'contact_email': None,
            'sec_url': 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001234576',
            'notable_investments': 'Major shareholder in most public companies',
            'decision_makers': 'Larry Fink (CEO)',
            'scraped_at': datetime.now().isoformat()
        }
    ]
    
    # Combine all
    all_investors = family_offices + vc_firms + institutional
    
    # Create DataFrame
    df = pd.DataFrame(all_investors)
    
    return df

def main():
    """Generate and save sample data"""
    print("=" * 70)
    print("🎯 GENERATING SAMPLE VC/FAMILY OFFICE DATABASE")
    print("=" * 70)
    print()
    
    df = generate_sample_data()
    
    # Save to CSV
    output_file = '/home/claude/vc_database_sample.csv'
    df.to_csv(output_file, index=False)
    
    # Summary
    print(f"✅ Generated {len(df)} sample investor records")
    print("\n📊 Breakdown by type:")
    print(df['type'].value_counts().to_string())
    
    print(f"\n💾 Saved to: {output_file}")
    
    # Display sample
    print("\n" + "=" * 70)
    print("📋 SAMPLE RECORDS")
    print("=" * 70)
    
    for idx, row in df.head(5).iterrows():
        print(f"\n{idx+1}. {row['name']}")
        print(f"   Type: {row['type']}")
        print(f"   AUM: {row['aum_estimate']}")
        print(f"   Focus: {row['investment_focus']}")
        print(f"   Sectors: {row['sectors']}")
        if row['notable_investments']:
            print(f"   Notable: {row['notable_investments']}")
    
    return df

if __name__ == "__main__":
    df = main()
