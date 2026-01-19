-- VC Intelligence Database Schema for Supabase
-- Run this in the Supabase SQL Editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing tables if they exist
DROP TABLE IF EXISTS portfolio_companies CASCADE;
DROP TABLE IF EXISTS investor_contacts CASCADE;
DROP TABLE IF EXISTS investors CASCADE;

-- Main investors table
CREATE TABLE investors (
    id SERIAL PRIMARY KEY,
    cik VARCHAR(20) UNIQUE,
    name VARCHAR(500) NOT NULL,
    type VARCHAR(100),
    address TEXT,
    city VARCHAR(200),
    state VARCHAR(10),
    zip VARCHAR(20),
    country VARCHAR(100) DEFAULT 'United States',

    -- Financial data
    aum_estimate VARCHAR(50),
    aum_min BIGINT,
    aum_max BIGINT,

    -- Investment strategy
    investment_focus TEXT,
    stage_preference VARCHAR(200),
    sectors TEXT,
    geography VARCHAR(500),
    check_size_min INTEGER,
    check_size_max INTEGER,

    -- Contact info
    website VARCHAR(500),
    contact_email VARCHAR(255),
    phone VARCHAR(50),
    linkedin_url VARCHAR(500),

    -- Intelligence
    notable_investments TEXT,
    decision_makers TEXT,
    investment_thesis TEXT,
    recent_activity TEXT,

    -- Metadata
    sec_url TEXT,
    crunchbase_url TEXT,
    data_sources TEXT[],
    data_quality_score INTEGER DEFAULT 0,

    -- Focus flags (for fast filtering)
    has_ai_focus BOOLEAN DEFAULT FALSE,
    has_music_focus BOOLEAN DEFAULT FALSE,
    has_fintech_focus BOOLEAN DEFAULT FALSE,

    -- Timestamps
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Key decision makers / contacts
CREATE TABLE investor_contacts (
    id SERIAL PRIMARY KEY,
    investor_id INTEGER REFERENCES investors(id) ON DELETE CASCADE,

    full_name VARCHAR(255) NOT NULL,
    title VARCHAR(200),
    email VARCHAR(255),
    linkedin_url VARCHAR(500),
    twitter_handle VARCHAR(100),

    role VARCHAR(100), -- 'GP', 'LP', 'Partner', 'Associate', 'Analyst'
    investment_focus TEXT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Portfolio companies (for VCs)
CREATE TABLE portfolio_companies (
    id SERIAL PRIMARY KEY,
    investor_id INTEGER REFERENCES investors(id) ON DELETE CASCADE,

    company_name VARCHAR(500) NOT NULL,
    company_website VARCHAR(500),
    industry VARCHAR(200),
    investment_date DATE,
    investment_round VARCHAR(50), -- 'Seed', 'Series A', etc.
    investment_amount BIGINT,
    current_status VARCHAR(100), -- 'Active', 'Exited', 'IPO', 'Acquired'
    exit_date DATE,
    exit_valuation BIGINT,

    source_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_investors_type ON investors(type);
CREATE INDEX idx_investors_state ON investors(state);
CREATE INDEX idx_investors_name ON investors(name);
CREATE INDEX idx_investors_ai_focus ON investors(has_ai_focus) WHERE has_ai_focus = TRUE;
CREATE INDEX idx_investors_fintech_focus ON investors(has_fintech_focus) WHERE has_fintech_focus = TRUE;
CREATE INDEX idx_investors_music_focus ON investors(has_music_focus) WHERE has_music_focus = TRUE;
CREATE INDEX idx_portfolio_investor ON portfolio_companies(investor_id);
CREATE INDEX idx_contacts_investor ON investor_contacts(investor_id);

-- Full text search index
CREATE INDEX idx_investors_search ON investors USING gin(
    to_tsvector('english', coalesce(name, '') || ' ' || coalesce(sectors, '') || ' ' || coalesce(investment_focus, ''))
);

-- Row Level Security (RLS)
ALTER TABLE investors ENABLE ROW LEVEL SECURITY;
ALTER TABLE investor_contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE portfolio_companies ENABLE ROW LEVEL SECURITY;

-- Public read access policies (for MVP)
CREATE POLICY "Allow public read access to investors"
    ON investors FOR SELECT
    USING (true);

CREATE POLICY "Allow public read access to contacts"
    ON investor_contacts FOR SELECT
    USING (true);

CREATE POLICY "Allow public read access to portfolio"
    ON portfolio_companies FOR SELECT
    USING (true);

-- Service role write access
CREATE POLICY "Allow service role insert on investors"
    ON investors FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Allow service role update on investors"
    ON investors FOR UPDATE
    USING (true);

-- Useful views
CREATE OR REPLACE VIEW v_family_offices AS
SELECT * FROM investors
WHERE type IN ('Family Office', 'Family Office / VC Hybrid')
ORDER BY aum_max DESC NULLS LAST;

CREATE OR REPLACE VIEW v_vc_firms AS
SELECT * FROM investors
WHERE type = 'Venture Capital'
ORDER BY aum_max DESC NULLS LAST;

CREATE OR REPLACE VIEW v_ai_investors AS
SELECT * FROM investors
WHERE has_ai_focus = TRUE
ORDER BY aum_max DESC NULLS LAST;

CREATE OR REPLACE VIEW v_fintech_investors AS
SELECT * FROM investors
WHERE has_fintech_focus = TRUE
ORDER BY aum_max DESC NULLS LAST;

-- Function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update timestamp
CREATE TRIGGER trg_investors_updated
    BEFORE UPDATE ON investors
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- Grant permissions
GRANT SELECT ON investors TO anon, authenticated;
GRANT SELECT ON investor_contacts TO anon, authenticated;
GRANT SELECT ON portfolio_companies TO anon, authenticated;
GRANT ALL ON investors TO service_role;
GRANT ALL ON investor_contacts TO service_role;
GRANT ALL ON portfolio_companies TO service_role;
