export interface Investor {
  id: number;
  cik: string;
  name: string;
  type: string;
  address: string;
  city: string;
  state: string;
  country: string;
  aum_estimate: string;
  aum_min: number;
  aum_max: number;
  investment_focus: string;
  stage_preference: string;
  sectors: string;
  geography: string;
  check_size_min: number;
  check_size_max: number;
  website: string;
  contact_email: string;
  phone: string;
  linkedin_url: string;
  notable_investments: string;
  decision_makers: string;
  investment_thesis: string;
  recent_activity: string;
  sec_url: string;
  crunchbase_url: string;
  data_sources: string[];
  data_quality_score: number;
  has_ai_focus: boolean;
  has_music_focus: boolean;
  has_fintech_focus: boolean;
  last_updated: string;
  scraped_at: string;
}

export interface InvestorContact {
  id: number;
  investor_id: number;
  full_name: string;
  title: string;
  email: string;
  linkedin_url: string;
  twitter_handle: string;
  role: string;
  investment_focus: string;
}

export interface PortfolioCompany {
  id: number;
  investor_id: number;
  company_name: string;
  company_website: string;
  industry: string;
  investment_date: string;
  investment_round: string;
  investment_amount: number;
  current_status: string;
  exit_date: string;
  exit_valuation: number;
}

export interface DatabaseStats {
  total_investors: number;
  by_type: Record<string, number>;
  top_states: Record<string, number>;
  ai_investors: number;
  music_investors: number;
  fintech_investors: number;
}

export interface SearchParams {
  investor_type?: string;
  sectors?: string[];
  state?: string;
  has_ai_focus?: boolean;
  has_music_focus?: boolean;
  has_fintech_focus?: boolean;
  limit?: number;
  offset?: number;
  search?: string;
}
