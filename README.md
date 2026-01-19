# VC Intelligence MCP

A comprehensive investor intelligence platform that scrapes SEC filings and provides MCP (Model Context Protocol) tools for searching VCs, family offices, and institutional investors.

## Features

- **SEC EDGAR Scraper** - Fetches Form ADV and 13F filings automatically
- **Investor Database** - Searchable database with 10,000+ investors
- **MCP Tools** - 6 built-in tools for AI agents to query investor data
- **Web Dashboard** - Modern Next.js frontend for browsing investors
- **Real-time Search** - Filter by type, sector, geography, and focus areas

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
| `/api/stats` | GET | Get database statistics |
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
