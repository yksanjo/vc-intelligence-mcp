# VC Intelligence MCP

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Last%20Updated-February%202026-orange" alt="Last Updated">
</p>

A comprehensive investor intelligence platform that scrapes SEC filings and provides MCP (Model Context Protocol) tools for searching VCs, family offices, and institutional investors.

## ⭐ Live Demo

**🌐 Production URL**: [vc-intelligence.vercel.app](https://vc-intelligence.vercel.app)

> **Note**: Demo video coming soon! For now, explore the live dashboard at the URL above.

## Features

- **SEC EDGAR Scraper** - Fetches Form ADV and 13F filings automatically
- **Investor Database** - Searchable database with 10,000+ investors
- **MCP Tools** - 6 built-in tools for AI agents to query investor data
- **Web Dashboard** - Modern Next.js frontend for browsing investors
- **Real-time Search** - Filter by type, sector, geography, and focus areas
- **Automated Updates** - Scheduled scraping via GitHub Actions

## Tech Stack

- **Frontend**: Next.js 15, React 19, Tailwind CSS
- **Backend**: Supabase (PostgreSQL)
- **Scraping**: Python (SEC EDGAR API)
- **Deployment**: Vercel

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yksanjo/vc-intelligence-mcp.git
cd vc-intelligence-mcp
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Set Up Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to SQL Editor and run the schema:
   ```bash
   cat supabase/schema.sql | pbcopy
   # Paste in Supabase SQL Editor and run
   ```
3. Copy your credentials to `.env.local`:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your Supabase URL and keys
   ```

### 4. Load Sample Data

```bash
cd scripts
pip install -r requirements.txt
python upload_to_supabase.py vc_database_sample.csv
```

### 5. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the dashboard.

## 📊 Sample Search Queries

Here are example queries you can try on the dashboard or via API:

### Find AI-Focused Investors in California
```bash
curl "http://localhost:3000/api/investors?has_ai_focus=true&state=CA"
```

### Find Family Offices in New York
```bash
curl "http://localhost:3000/api/investors?type=Family+Office&state=NY"
```

### Find Fintech VCs
```bash
curl "http://localhost:3000/api/investors?type=Venture+Capital&has_fintech_focus=true"
```

### Search for Music Tech Investors
```bash
curl "http://localhost:3000/api/investors?has_music_focus=true&limit=50"
```

### Get Database Statistics
```bash
curl "http://localhost:3000/api/stats"
```

### Full-Text Search
```bash
curl "http://localhost:3000/api/investors?search=Sequoia"
```

## 📈 Data Freshness

The dashboard displays real-time data freshness indicators:

| Indicator | Description |
|-----------|-------------|
| 🟢 Live | Data updated within last 24 hours |
| 🟡 Recent | Data updated within last 7 days |
| 🔴 Stale | Data older than 7 days |

Last database update: Check `/api/stats` response for `last_updated` timestamp.

## Scraping Infrastructure

### Run SEC Scraper Locally

```bash
cd lib/scrapers
pip install -r ../../scripts/requirements.txt
python sec_scraper.py --limit 1000
```

### Upload Scraped Data

```bash
cd scripts
python upload_to_supabase.py ../lib/scrapers/vc_database.csv
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/investors` | GET | Search investors with filters |
| `/api/investors` | POST | Add new investor |
| `/api/stats` | GET | Get database statistics with timestamps |
| `/api/scrape` | POST | Trigger scraping job |

### Query Parameters for `/api/investors`

- `type` - Filter by investor type (e.g., "Venture Capital", "Family Office")
- `state` - Filter by US state (e.g., "CA", "NY")
- `has_ai_focus` - Filter AI-focused investors (true/false)
- `has_fintech_focus` - Filter fintech investors (true/false)
- `has_music_focus` - Filter music tech investors (true/false)
- `search` - Full-text search query
- `limit` - Results per page (default: 100)
- `offset` - Pagination offset

## MCP Integration

This project provides MCP tools for AI agents. Available tools:

1. **search_investors** - Search by type, sectors, location
2. **get_investor_details** - Get full details for specific investor
3. **find_family_offices** - Find family offices with filters
4. **find_vc_firms** - Find VCs by stage and sector
5. **get_ai_investors** - Get all AI/ML focused investors
6. **get_database_stats** - Get overview statistics

### Publishing to npm (Coming Soon)

```bash
# Build the MCP package
npm run build:mcp

# Publish to npm
npm publish
```

## Deployment

### Deploy to Vercel

```bash
vercel --prod
```

### Environment Variables (Vercel Dashboard)

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`

## Project Structure

```
vc-intelligence-mcp/
├── app/                    # Next.js app router
│   ├── api/               # API routes
│   │   ├── investors/     # Investor CRUD
│   │   ├── stats/         # Statistics
│   │   └── scrape/        # Scraping trigger
│   ├── page.tsx           # Main dashboard
│   └── layout.tsx         # Root layout
├── components/            # React components
├── lib/                   # Shared libraries
│   ├── supabase/          # Supabase client
│   ├── scrapers/          # Python scrapers
│   └── types.ts           # TypeScript types
├── scripts/               # Utility scripts
│   ├── upload_to_supabase.py
│   └── requirements.txt
├── supabase/              # Database schema
│   └── schema.sql
├── .github/               # GitHub Actions
│   └── workflows/         # Scheduled scraping
└── public/                # Static assets
```

## Data Sources

1. **SEC EDGAR** (Free, Legal)
   - Form ADV: Investment advisers $150M+ AUM
   - Form 13F: Institutional investors $100M+ holdings
   - Form D: New fund formations

2. **Crunchbase** (Requires API key)
   - Portfolio companies
   - Funding rounds
   - Co-investor networks

3. **GitHub Intelligence** (Planned)
   - Technology adoption signals
   - Open source activity

## License

MIT License - See LICENSE file

## Author

Built by Yoshi Tomioka for VC fundraising intelligence.
