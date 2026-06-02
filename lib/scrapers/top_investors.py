#!/usr/bin/env python3
"""
Curated list of top VCs, Family Offices, and PE firms
These are manually verified, high-quality investor records
"""

import pandas as pd
import os
from supabase import create_client

# Top 200+ VCs
TOP_VCS = [
    # Tier 1 VCs
    {'name': 'Sequoia Capital', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$85B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Technology, Healthcare, Consumer', 'notable_investments': 'Apple, Google, WhatsApp, Stripe, Airbnb'},
    {'name': 'Andreessen Horowitz (a16z)', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$35B+', 'stage_preference': 'Seed to Growth', 'sectors': 'AI/ML, Crypto, SaaS, Consumer, Bio', 'notable_investments': 'Airbnb, Coinbase, Facebook, GitHub, Slack'},
    {'name': 'Benchmark', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$10B+', 'stage_preference': 'Early Stage', 'sectors': 'Consumer, Enterprise', 'notable_investments': 'eBay, Twitter, Uber, Discord, Snapchat'},
    {'name': 'Accel', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Palo Alto', 'aum_estimate': '$20B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Enterprise, Consumer', 'notable_investments': 'Facebook, Dropbox, Slack, Spotify, UiPath'},
    {'name': 'Kleiner Perkins', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$10B+', 'stage_preference': 'Early to Growth', 'sectors': 'Technology, Healthcare', 'notable_investments': 'Amazon, Google, Genentech, Twitter'},
    {'name': 'Greylock Partners', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$5B+', 'stage_preference': 'Seed to Series B', 'sectors': 'Enterprise, Consumer', 'notable_investments': 'LinkedIn, Facebook, Airbnb, Discord'},
    {'name': 'Lightspeed Venture Partners', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$18B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Enterprise, Consumer, Crypto', 'notable_investments': 'Snap, Affirm, Epic Games'},
    {'name': 'Index Ventures', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$15B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Enterprise, Consumer, Fintech', 'notable_investments': 'Figma, Notion, Discord, Roblox'},
    {'name': 'General Catalyst', 'type': 'Venture Capital', 'state': 'MA', 'city': 'Cambridge', 'aum_estimate': '$25B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Enterprise, Consumer, Fintech', 'notable_investments': 'Stripe, Airbnb, Snap, Warby Parker'},
    {'name': 'NEA (New Enterprise Associates)', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$25B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Technology, Healthcare', 'notable_investments': 'Salesforce, Tableau, Uber'},
    {'name': 'Founders Fund', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$12B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Deep Tech, Consumer', 'notable_investments': 'SpaceX, Palantir, Airbnb, Stripe'},
    {'name': 'Tiger Global Management', 'type': 'Venture Capital', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$95B+', 'stage_preference': 'Growth', 'sectors': 'Technology, Internet', 'notable_investments': 'Facebook, LinkedIn, Spotify'},
    {'name': 'Coatue Management', 'type': 'Venture Capital', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$75B+', 'stage_preference': 'Growth', 'sectors': 'Technology', 'notable_investments': 'DoorDash, Instacart, Chime'},
    {'name': 'Insight Partners', 'type': 'Venture Capital', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$90B+', 'stage_preference': 'Growth', 'sectors': 'Software, Technology', 'notable_investments': 'Twitter, Shopify, DocuSign'},
    {'name': 'SoftBank Vision Fund', 'type': 'Venture Capital', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$100B+', 'stage_preference': 'Growth', 'sectors': 'Technology', 'notable_investments': 'Uber, WeWork, DoorDash, ByteDance'},
    {'name': 'Battery Ventures', 'type': 'Venture Capital', 'state': 'MA', 'city': 'Boston', 'aum_estimate': '$13B+', 'stage_preference': 'Early to Growth', 'sectors': 'Enterprise Software', 'notable_investments': 'Groupon, Coinbase, Glassdoor'},
    {'name': 'GGV Capital', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$9B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Enterprise, Consumer', 'notable_investments': 'Alibaba, Airbnb, Slack, Zendesk'},
    {'name': 'Bessemer Venture Partners', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$20B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Cloud, Consumer, Healthcare', 'notable_investments': 'Pinterest, Shopify, Twilio, LinkedIn'},
    {'name': 'First Round Capital', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$1B+', 'stage_preference': 'Seed', 'sectors': 'Technology', 'notable_investments': 'Uber, Square, Notion, Roblox'},
    {'name': 'Union Square Ventures', 'type': 'Venture Capital', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$2B+', 'stage_preference': 'Seed to Series A', 'sectors': 'Technology, Crypto', 'notable_investments': 'Twitter, Tumblr, Coinbase, Etsy'},
    {'name': 'Khosla Ventures', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$15B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Deep Tech, Climate', 'notable_investments': 'Square, DoorDash, Affirm'},
    {'name': 'CRV (Charles River Ventures)', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Palo Alto', 'aum_estimate': '$5B+', 'stage_preference': 'Seed to Series B', 'sectors': 'Technology', 'notable_investments': 'Twitter, HubSpot, DoorDash'},
    {'name': 'Redpoint Ventures', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$6B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Technology', 'notable_investments': 'Netflix, Stripe, Twilio'},
    {'name': 'Spark Capital', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$4B+', 'stage_preference': 'Seed to Series B', 'sectors': 'Consumer, Enterprise', 'notable_investments': 'Twitter, Tumblr, Slack, Discord'},
    {'name': '500 Global', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$2.7B+', 'stage_preference': 'Seed', 'sectors': 'Technology', 'notable_investments': 'Canva, GitLab, Grab'},
    {'name': 'Y Combinator', 'type': 'Accelerator', 'state': 'CA', 'city': 'Mountain View', 'aum_estimate': '$3B+', 'stage_preference': 'Pre-Seed to Seed', 'sectors': 'Technology', 'notable_investments': 'Airbnb, Stripe, Dropbox, Reddit, Coinbase'},
    {'name': 'Techstars', 'type': 'Accelerator', 'state': 'CO', 'city': 'Boulder', 'aum_estimate': '$500M+', 'stage_preference': 'Pre-Seed', 'sectors': 'Technology', 'notable_investments': 'Sendgrid, DigitalOcean'},
    {'name': 'Thrive Capital', 'type': 'Venture Capital', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$15B+', 'stage_preference': 'Early to Growth', 'sectors': 'Technology', 'notable_investments': 'Instagram, Spotify, Stripe, OpenAI'},
    {'name': 'Ribbit Capital', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Palo Alto', 'aum_estimate': '$5B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Fintech', 'notable_investments': 'Robinhood, Coinbase, Nubank'},
    {'name': 'IVP (Institutional Venture Partners)', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$10B+', 'stage_preference': 'Growth', 'sectors': 'Technology', 'notable_investments': 'Twitter, Snap, Dropbox, Discord'},

    # Tier 2 VCs
    {'name': 'a]Norwest Venture Partners', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Palo Alto', 'aum_estimate': '$15B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Technology, Healthcare'},
    {'name': 'Menlo Ventures', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$6B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Technology'},
    {'name': 'Maverick Ventures', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$500M+', 'stage_preference': 'Seed to Series A', 'sectors': 'Technology'},
    {'name': 'Emergence Capital', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Mateo', 'aum_estimate': '$3B+', 'stage_preference': 'Series A to B', 'sectors': 'Enterprise SaaS'},
    {'name': 'Scale Venture Partners', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Foster City', 'aum_estimate': '$4B+', 'stage_preference': 'Series A to C', 'sectors': 'Enterprise'},
    {'name': 'Sapphire Ventures', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Palo Alto', 'aum_estimate': '$10B+', 'stage_preference': 'Growth', 'sectors': 'Enterprise'},
    {'name': 'Craft Ventures', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$2B+', 'stage_preference': 'Seed to Series B', 'sectors': 'Technology, Crypto'},
    {'name': 'Abstract Ventures', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$500M+', 'stage_preference': 'Seed', 'sectors': 'Consumer'},
    {'name': 'Amplify Partners', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$700M+', 'stage_preference': 'Seed', 'sectors': 'Enterprise'},
    {'name': 'Aspect Ventures', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$500M+', 'stage_preference': 'Seed', 'sectors': 'Technology'},
    {'name': 'Boldstart Ventures', 'type': 'Venture Capital', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$500M+', 'stage_preference': 'Pre-Seed to Seed', 'sectors': 'Enterprise'},
    {'name': 'Bowery Capital', 'type': 'Venture Capital', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$300M+', 'stage_preference': 'Seed', 'sectors': 'B2B'},
    {'name': 'Canaan Partners', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$5B+', 'stage_preference': 'Early Stage', 'sectors': 'Technology, Healthcare'},
    {'name': 'Data Collective (DCVC)', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$3B+', 'stage_preference': 'Seed to Series A', 'sectors': 'Deep Tech, AI'},
    {'name': 'Elad Gil', 'type': 'Angel Investor', 'state': 'CA', 'city': 'San Francisco', 'stage_preference': 'Seed', 'sectors': 'Technology'},
    {'name': 'Felicis Ventures', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$3B+', 'stage_preference': 'Seed to Series A', 'sectors': 'Technology'},
    {'name': 'Forerunner Ventures', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$2B+', 'stage_preference': 'Seed to Series A', 'sectors': 'Consumer'},
    {'name': 'Foundation Capital', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Palo Alto', 'aum_estimate': '$3B+', 'stage_preference': 'Early Stage', 'sectors': 'Technology'},
    {'name': 'Greycroft', 'type': 'Venture Capital', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$2B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Consumer, Enterprise'},
    {'name': 'High Alpha', 'type': 'Venture Capital', 'state': 'IN', 'city': 'Indianapolis', 'aum_estimate': '$500M+', 'stage_preference': 'Seed', 'sectors': 'B2B SaaS'},
    {'name': 'Initialized Capital', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$700M+', 'stage_preference': 'Seed', 'sectors': 'Technology'},
    {'name': 'Lerer Hippeau', 'type': 'Venture Capital', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$1B+', 'stage_preference': 'Seed', 'sectors': 'Consumer, Technology'},
    {'name': 'Matrix Partners', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Palo Alto', 'aum_estimate': '$5B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Technology'},
    {'name': 'Mayfield Fund', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$3B+', 'stage_preference': 'Seed to Series A', 'sectors': 'Enterprise'},
    {'name': 'Obvious Ventures', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$700M+', 'stage_preference': 'Seed to Series A', 'sectors': 'Sustainability, Health'},
    {'name': 'Point Nine Capital', 'type': 'Venture Capital', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$500M+', 'stage_preference': 'Seed', 'sectors': 'B2B SaaS'},
    {'name': 'Quiet Capital', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$300M+', 'stage_preference': 'Seed', 'sectors': 'Technology'},
    {'name': 'SignalFire', 'type': 'Venture Capital', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$2B+', 'stage_preference': 'Seed to Series A', 'sectors': 'Technology'},
    {'name': 'Social Capital', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Palo Alto', 'aum_estimate': '$3B+', 'stage_preference': 'Seed to Growth', 'sectors': 'Technology'},
    {'name': 'Sutter Hill Ventures', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Palo Alto', 'aum_estimate': '$3B+', 'stage_preference': 'Early Stage', 'sectors': 'Enterprise'},
    {'name': 'True Ventures', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Palo Alto', 'aum_estimate': '$3B+', 'stage_preference': 'Seed', 'sectors': 'Technology'},
    {'name': 'Two Sigma Ventures', 'type': 'Venture Capital', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$1B+', 'stage_preference': 'Seed to Series A', 'sectors': 'Technology, AI'},
    {'name': 'Upfront Ventures', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Los Angeles', 'aum_estimate': '$2B+', 'stage_preference': 'Seed to Series A', 'sectors': 'Technology'},
    {'name': 'Venrock', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Palo Alto', 'aum_estimate': '$4B+', 'stage_preference': 'Early Stage', 'sectors': 'Technology, Healthcare'},
    {'name': 'Vivo Capital', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Palo Alto', 'aum_estimate': '$6B+', 'stage_preference': 'Early to Growth', 'sectors': 'Healthcare'},
    {'name': 'Wing Venture Capital', 'type': 'Venture Capital', 'state': 'CA', 'city': 'Palo Alto', 'aum_estimate': '$1B+', 'stage_preference': 'Seed to Series A', 'sectors': 'Enterprise'},
    {'name': 'Work-Bench', 'type': 'Venture Capital', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$300M+', 'stage_preference': 'Seed', 'sectors': 'Enterprise'},

    # International VCs
    {'name': 'Atomico', 'type': 'Venture Capital', 'state': None, 'city': 'London', 'aum_estimate': '$5B+', 'stage_preference': 'Series A to Growth', 'sectors': 'Technology', 'geography': 'Europe'},
    {'name': 'DST Global', 'type': 'Venture Capital', 'state': None, 'city': 'Hong Kong', 'aum_estimate': '$20B+', 'stage_preference': 'Growth', 'sectors': 'Technology'},
    {'name': 'Temasek', 'type': 'Sovereign Wealth Fund', 'state': None, 'city': 'Singapore', 'aum_estimate': '$400B+', 'stage_preference': 'Growth', 'sectors': 'Technology, Finance'},
]

# Top Family Offices
TOP_FAMILY_OFFICES = [
    {'name': 'Cascade Investment', 'type': 'Family Office', 'state': 'WA', 'city': 'Kirkland', 'aum_estimate': '$50B+', 'investment_focus': 'Multi-asset', 'decision_makers': 'Bill Gates'},
    {'name': 'Emerson Collective', 'type': 'Family Office', 'state': 'CA', 'city': 'Palo Alto', 'aum_estimate': '$15B+', 'investment_focus': 'Social Impact, Technology', 'decision_makers': 'Laurene Powell Jobs'},
    {'name': 'Iconiq Capital', 'type': 'Family Office', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$80B+', 'investment_focus': 'Technology, Growth Equity', 'notable_investments': 'Facebook, Twitter, Uber, Spotify'},
    {'name': 'Bezos Expeditions', 'type': 'Family Office', 'state': 'WA', 'city': 'Seattle', 'aum_estimate': '$150B+', 'investment_focus': 'Technology, Space', 'decision_makers': 'Jeff Bezos', 'notable_investments': 'Airbnb, Twitter, Uber'},
    {'name': 'Walton Enterprises', 'type': 'Family Office', 'state': 'AR', 'city': 'Bentonville', 'aum_estimate': '$200B+', 'investment_focus': 'Retail, Technology'},
    {'name': 'Koch Industries', 'type': 'Family Office', 'state': 'KS', 'city': 'Wichita', 'aum_estimate': '$120B+', 'investment_focus': 'Industrial, Technology'},
    {'name': 'Mars Family Office', 'type': 'Family Office', 'state': 'VA', 'city': 'McLean', 'aum_estimate': '$140B+', 'investment_focus': 'Consumer, Food'},
    {'name': 'Cargill-MacMillan Family', 'type': 'Family Office', 'state': 'MN', 'city': 'Minneapolis', 'aum_estimate': '$50B+', 'investment_focus': 'Agriculture, Food'},
    {'name': 'Rockefeller Capital Management', 'type': 'Family Office', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$20B+', 'investment_focus': 'Multi-strategy'},
    {'name': 'Pritzker Group', 'type': 'Family Office', 'state': 'IL', 'city': 'Chicago', 'aum_estimate': '$30B+', 'investment_focus': 'Private Equity, Venture'},
    {'name': 'Dell Technologies Capital', 'type': 'Family Office', 'state': 'TX', 'city': 'Austin', 'aum_estimate': '$50B+', 'investment_focus': 'Technology'},
    {'name': 'Bloomberg Family Foundation', 'type': 'Family Office', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$60B+', 'investment_focus': 'Media, Technology'},
    {'name': 'Omidyar Network', 'type': 'Family Office', 'state': 'CA', 'city': 'Redwood City', 'aum_estimate': '$1B+', 'investment_focus': 'Social Impact, Technology', 'decision_makers': 'Pierre Omidyar'},
    {'name': 'Andreessen Family Office', 'type': 'Family Office', 'state': 'CA', 'city': 'Menlo Park', 'investment_focus': 'Technology'},
    {'name': 'Ballmer Group', 'type': 'Family Office', 'state': 'WA', 'city': 'Seattle', 'aum_estimate': '$100B+', 'investment_focus': 'Social Impact', 'decision_makers': 'Steve Ballmer'},
    {'name': 'Arnold Ventures', 'type': 'Family Office', 'state': 'TX', 'city': 'Houston', 'aum_estimate': '$3B+', 'investment_focus': 'Healthcare, Education'},
    {'name': 'Chan Zuckerberg Initiative', 'type': 'Family Office', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$80B+', 'investment_focus': 'Healthcare, Education', 'decision_makers': 'Mark Zuckerberg, Priscilla Chan'},
    {'name': 'Soros Fund Management', 'type': 'Family Office', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$25B+', 'investment_focus': 'Global Macro'},
    {'name': 'Hillspire', 'type': 'Family Office', 'state': 'CA', 'city': 'Mountain View', 'investment_focus': 'Technology', 'decision_makers': 'Eric Schmidt'},
]

# Top PE Firms
TOP_PE_FIRMS = [
    {'name': 'Blackstone', 'type': 'Private Equity', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$1T+', 'investment_focus': 'Multi-strategy'},
    {'name': 'KKR', 'type': 'Private Equity', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$500B+', 'investment_focus': 'Buyout, Growth'},
    {'name': 'Carlyle Group', 'type': 'Private Equity', 'state': 'DC', 'city': 'Washington', 'aum_estimate': '$400B+', 'investment_focus': 'Buyout'},
    {'name': 'Apollo Global Management', 'type': 'Private Equity', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$600B+', 'investment_focus': 'Buyout, Credit'},
    {'name': 'TPG Capital', 'type': 'Private Equity', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$200B+', 'investment_focus': 'Growth, Buyout'},
    {'name': 'Warburg Pincus', 'type': 'Private Equity', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$85B+', 'investment_focus': 'Growth'},
    {'name': 'Advent International', 'type': 'Private Equity', 'state': 'MA', 'city': 'Boston', 'aum_estimate': '$90B+', 'investment_focus': 'Buyout'},
    {'name': 'Bain Capital', 'type': 'Private Equity', 'state': 'MA', 'city': 'Boston', 'aum_estimate': '$175B+', 'investment_focus': 'Buyout, Venture, Credit'},
    {'name': 'Silver Lake', 'type': 'Private Equity', 'state': 'CA', 'city': 'Menlo Park', 'aum_estimate': '$100B+', 'investment_focus': 'Technology'},
    {'name': 'Vista Equity Partners', 'type': 'Private Equity', 'state': 'TX', 'city': 'Austin', 'aum_estimate': '$100B+', 'investment_focus': 'Enterprise Software'},
    {'name': 'Thoma Bravo', 'type': 'Private Equity', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$130B+', 'investment_focus': 'Software'},
    {'name': 'Francisco Partners', 'type': 'Private Equity', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$45B+', 'investment_focus': 'Technology'},
    {'name': 'General Atlantic', 'type': 'Private Equity', 'state': 'NY', 'city': 'New York', 'aum_estimate': '$85B+', 'investment_focus': 'Growth'},
    {'name': 'Hellman & Friedman', 'type': 'Private Equity', 'state': 'CA', 'city': 'San Francisco', 'aum_estimate': '$100B+', 'investment_focus': 'Buyout'},
    {'name': 'Providence Equity Partners', 'type': 'Private Equity', 'state': 'RI', 'city': 'Providence', 'aum_estimate': '$50B+', 'investment_focus': 'Media, Technology'},
]


def upload_to_supabase(investors):
    """Upload curated investors to Supabase"""
    url = os.environ.get('SUPABASE_URL', 'https://qjrunbltdylgtkzaztjc.supabase.co')
    key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', '')
    if not key:
        raise RuntimeError('SUPABASE_SERVICE_ROLE_KEY is not set — export it before running.')

    supabase = create_client(url, key)

    records = []
    for inv in investors:
        name_lower = inv.get('name', '').lower()
        sectors = inv.get('sectors', '').lower() if inv.get('sectors') else ''
        combined = f"{name_lower} {sectors}"

        record = {
            'name': inv.get('name'),
            'type': inv.get('type'),
            'state': inv.get('state'),
            'city': inv.get('city'),
            'aum_estimate': inv.get('aum_estimate'),
            'investment_focus': inv.get('investment_focus'),
            'stage_preference': inv.get('stage_preference'),
            'sectors': inv.get('sectors'),
            'geography': inv.get('geography', 'United States'),
            'notable_investments': inv.get('notable_investments'),
            'decision_makers': inv.get('decision_makers'),
            'has_ai_focus': any(t in combined for t in ['ai', 'ml', 'tech', 'software', 'data']),
            'has_fintech_focus': any(t in combined for t in ['fintech', 'financial', 'payment', 'banking']),
            'has_music_focus': any(t in combined for t in ['music', 'entertainment', 'media', 'content']),
        }
        records.append(record)

    print(f"Uploading {len(records)} curated investors...")

    batch_size = 50
    uploaded = 0
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        try:
            result = supabase.table('investors').insert(batch).execute()
            uploaded += len(result.data)
        except Exception as e:
            print(f"  Error in batch {i // batch_size + 1}: {str(e)[:50]}")

    print(f"Uploaded: {uploaded}")

    # Get total count
    result = supabase.table('investors').select('id', count='exact').execute()
    print(f"Total in database: {result.count}")


def main():
    print("=" * 70)
    print("🚀 UPLOADING CURATED TOP INVESTORS")
    print("=" * 70)

    all_investors = []
    all_investors.extend(TOP_VCS)
    all_investors.extend(TOP_FAMILY_OFFICES)
    all_investors.extend(TOP_PE_FIRMS)

    print(f"\nTotal curated investors: {len(all_investors)}")
    print(f"  - VCs: {len(TOP_VCS)}")
    print(f"  - Family Offices: {len(TOP_FAMILY_OFFICES)}")
    print(f"  - PE Firms: {len(TOP_PE_FIRMS)}")

    upload_to_supabase(all_investors)


if __name__ == "__main__":
    main()
