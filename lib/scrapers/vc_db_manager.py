#!/usr/bin/env python3
"""
VC Database Manager
Load CSV data into SQLite database and provide query interface
"""

import sqlite3
import pandas as pd
import re
from typing import List, Dict, Optional
from datetime import datetime

class VCDatabase:
    """Manage VC intelligence database"""
    
    def __init__(self, db_path: str = '/home/claude/vc_intelligence.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None
        self.setup_database()
    
    def setup_database(self):
        """Create database and tables"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Return dict-like rows
        
        # Create tables
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS investors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cik TEXT UNIQUE,
                name TEXT NOT NULL,
                type TEXT,
                address TEXT,
                aum_estimate TEXT,
                investment_focus TEXT,
                stage_preference TEXT,
                sectors TEXT,
                geography TEXT,
                website TEXT,
                contact_email TEXT,
                sec_url TEXT,
                notable_investments TEXT,
                decision_makers TEXT,
                scraped_at TEXT,
                
                -- Parsed fields for filtering
                state TEXT,
                city TEXT,
                has_ai_focus INTEGER DEFAULT 0,
                has_music_focus INTEGER DEFAULT 0,
                has_fintech_focus INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_investor_type ON investors(type)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_state ON investors(state)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_ai_focus ON investors(has_ai_focus)
        ''')
        
        self.conn.commit()
    
    def load_from_csv(self, csv_path: str):
        """Load investor data from CSV"""
        print(f"📂 Loading data from {csv_path}...")
        
        df = pd.read_csv(csv_path)
        
        # Parse additional fields
        for idx, row in df.iterrows():
            # Extract state from address
            state = self._extract_state(row.get('address', ''))
            city = self._extract_city(row.get('address', ''))
            
            # Check sector focus
            sectors = str(row.get('sectors', '')).lower()
            has_ai = 1 if any(term in sectors for term in ['ai', 'ml', 'machine learning', 'artificial intelligence']) else 0
            has_music = 1 if 'music' in sectors else 0
            has_fintech = 1 if 'fintech' in sectors or 'finance' in sectors else 0
            
            df.at[idx, 'state'] = state
            df.at[idx, 'city'] = city
            df.at[idx, 'has_ai_focus'] = has_ai
            df.at[idx, 'has_music_focus'] = has_music
            df.at[idx, 'has_fintech_focus'] = has_fintech
        
        # Load into database
        df.to_sql('investors', self.conn, if_exists='replace', index=False)
        
        print(f"✅ Loaded {len(df)} investors into database")
        
        return len(df)
    
    def _extract_state(self, address: str) -> Optional[str]:
        """Extract state code from address"""
        if not address:
            return None
        
        # Look for state patterns like "NY", "CA 94025"
        state_pattern = r'\b([A-Z]{2})\b'
        matches = re.findall(state_pattern, address)
        
        # Common state codes
        states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
        
        for match in matches:
            if match in states:
                return match
        
        return None
    
    def _extract_city(self, address: str) -> Optional[str]:
        """Extract city from address"""
        if not address:
            return None
        
        # Simple extraction - take first part before comma
        parts = address.split(',')
        if len(parts) > 0:
            city = parts[0].strip()
            # Remove street addresses
            if any(char.isdigit() for char in city):
                if len(parts) > 1:
                    return parts[1].strip()
            return city
        
        return None
    
    def search_investors(self, 
                        investor_type: Optional[str] = None,
                        sectors: Optional[List[str]] = None,
                        state: Optional[str] = None,
                        has_ai_focus: bool = False,
                        has_music_focus: bool = False,
                        has_fintech_focus: bool = False,
                        limit: int = 100) -> List[Dict]:
        """
        Search for investors with filters
        
        Args:
            investor_type: 'Family Office', 'Venture Capital', etc.
            sectors: List of sector keywords to search for
            state: Two-letter state code
            has_ai_focus: Filter for AI/ML investors
            has_music_focus: Filter for music tech investors
            has_fintech_focus: Filter for fintech investors
            limit: Maximum results to return
        
        Returns:
            List of investor dictionaries
        """
        query = "SELECT * FROM investors WHERE 1=1"
        params = []
        
        if investor_type:
            query += " AND type = ?"
            params.append(investor_type)
        
        if state:
            query += " AND state = ?"
            params.append(state)
        
        if has_ai_focus:
            query += " AND has_ai_focus = 1"
        
        if has_music_focus:
            query += " AND has_music_focus = 1"
        
        if has_fintech_focus:
            query += " AND has_fintech_focus = 1"
        
        if sectors:
            for sector in sectors:
                query += " AND (sectors LIKE ? OR investment_focus LIKE ?)"
                params.extend([f'%{sector}%', f'%{sector}%'])
        
        query += f" LIMIT {limit}"
        
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        
        results = [dict(row) for row in cursor.fetchall()]
        return results
    
    def get_family_offices(self, min_aum: Optional[str] = None) -> List[Dict]:
        """Get all family offices"""
        return self.search_investors(investor_type='Family Office')
    
    def get_vc_firms(self) -> List[Dict]:
        """Get all VC firms"""
        return self.search_investors(investor_type='Venture Capital')
    
    def get_ai_investors(self) -> List[Dict]:
        """Get investors focused on AI/ML"""
        return self.search_investors(has_ai_focus=True)
    
    def get_music_tech_investors(self) -> List[Dict]:
        """Get investors focused on music tech"""
        return self.search_investors(has_music_focus=True)
    
    def get_fintech_investors(self) -> List[Dict]:
        """Get investors focused on fintech"""
        return self.search_investors(has_fintech_focus=True)
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Total count
        cursor.execute("SELECT COUNT(*) FROM investors")
        stats['total_investors'] = cursor.fetchone()[0]
        
        # By type
        cursor.execute("SELECT type, COUNT(*) FROM investors GROUP BY type")
        stats['by_type'] = {row[0]: row[1] for row in cursor.fetchall()}
        
        # By state
        cursor.execute("SELECT state, COUNT(*) FROM investors WHERE state IS NOT NULL GROUP BY state ORDER BY COUNT(*) DESC LIMIT 10")
        stats['top_states'] = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Focus areas
        cursor.execute("SELECT COUNT(*) FROM investors WHERE has_ai_focus = 1")
        stats['ai_investors'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM investors WHERE has_music_focus = 1")
        stats['music_investors'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM investors WHERE has_fintech_focus = 1")
        stats['fintech_investors'] = cursor.fetchone()[0]
        
        return stats
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

def main():
    """Demo the database system"""
    print("=" * 70)
    print("🗄️  VC INTELLIGENCE DATABASE MANAGER")
    print("=" * 70)
    print()
    
    # Initialize database
    db = VCDatabase()
    
    # Load sample data
    csv_path = '/home/claude/vc_database_sample.csv'
    db.load_from_csv(csv_path)
    
    # Show stats
    print("\n📊 DATABASE STATISTICS")
    print("-" * 70)
    stats = db.get_stats()
    print(f"Total Investors: {stats['total_investors']}")
    print("\nBy Type:")
    for inv_type, count in stats['by_type'].items():
        print(f"  {inv_type}: {count}")
    
    print(f"\nSpecialty Focus:")
    print(f"  AI/ML Investors: {stats['ai_investors']}")
    print(f"  Music Tech Investors: {stats['music_investors']}")
    print(f"  Fintech Investors: {stats['fintech_investors']}")
    
    # Example queries
    print("\n" + "=" * 70)
    print("🔍 EXAMPLE QUERIES")
    print("=" * 70)
    
    print("\n1️⃣  Family Offices:")
    print("-" * 70)
    family_offices = db.get_family_offices()
    for fo in family_offices[:3]:
        print(f"• {fo['name']}")
        print(f"  AUM: {fo['aum_estimate']}")
        print(f"  Focus: {fo['investment_focus']}")
        print()
    
    print("\n2️⃣  AI/ML Focused Investors:")
    print("-" * 70)
    ai_investors = db.get_ai_investors()
    for inv in ai_investors[:3]:
        print(f"• {inv['name']} ({inv['type']})")
        print(f"  Sectors: {inv['sectors']}")
        print()
    
    print("\n3️⃣  California VCs:")
    print("-" * 70)
    ca_vcs = db.search_investors(investor_type='Venture Capital', state='CA')
    for vc in ca_vcs[:3]:
        print(f"• {vc['name']}")
        print(f"  Location: {vc['city']}, {vc['state']}")
        print(f"  Notable: {vc['notable_investments'][:100]}...")
        print()
    
    # Save database info
    print("\n" + "=" * 70)
    print("💾 DATABASE SAVED")
    print("=" * 70)
    print(f"Location: {db.db_path}")
    print("\nYou can query it with:")
    print("  sqlite3 vc_intelligence.db")
    print("\nOr use Python:")
    print("  from vc_db_manager import VCDatabase")
    print("  db = VCDatabase()")
    print("  results = db.search_investors(has_ai_focus=True)")
    
    db.close()

if __name__ == "__main__":
    main()
