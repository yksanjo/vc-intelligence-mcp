"use client";

import { useState, useEffect } from "react";
import { Search, Building2, Users, TrendingUp, Database, Filter, RefreshCw } from "lucide-react";
import InvestorCard from "@/components/InvestorCard";
import StatsCard from "@/components/StatsCard";

interface Investor {
  id: number;
  name: string;
  type: string;
  aum_estimate: string;
  investment_focus: string;
  sectors: string;
  state: string;
  notable_investments: string;
  decision_makers: string;
  website: string;
}

interface Stats {
  total_investors: number;
  by_type: Record<string, number>;
  ai_investors: number;
  fintech_investors: number;
  music_investors: number;
}

export default function Home() {
  const [investors, setInvestors] = useState<Investor[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterType, setFilterType] = useState<string>("");
  const [filterFocus, setFilterFocus] = useState<string>("");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [investorsRes, statsRes] = await Promise.all([
        fetch("/api/investors"),
        fetch("/api/stats"),
      ]);

      if (investorsRes.ok) {
        const data = await investorsRes.json();
        setInvestors(data.investors || []);
      }

      if (statsRes.ok) {
        const data = await statsRes.json();
        setStats(data);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredInvestors = investors.filter((investor) => {
    const matchesSearch =
      !searchQuery ||
      investor.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      investor.sectors?.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesType = !filterType || investor.type === filterType;

    const matchesFocus =
      !filterFocus ||
      (filterFocus === "ai" && investor.sectors?.toLowerCase().includes("ai")) ||
      (filterFocus === "fintech" && investor.sectors?.toLowerCase().includes("fintech")) ||
      (filterFocus === "music" && investor.sectors?.toLowerCase().includes("music"));

    return matchesSearch && matchesType && matchesFocus;
  });

  return (
    <main className="min-h-screen bg-[#0a0a0a]">
      {/* Header */}
      <header className="border-b border-gray-800 bg-[#111]">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Database className="w-8 h-8 text-blue-500" />
              <div>
                <h1 className="text-2xl font-bold text-white">VC Intelligence</h1>
                <p className="text-sm text-gray-400">MCP-Powered Investor Search</p>
              </div>
            </div>
            <button
              onClick={fetchData}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
              Refresh
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <StatsCard
            icon={<Building2 className="w-6 h-6" />}
            label="Total Investors"
            value={stats?.total_investors || 0}
            color="blue"
          />
          <StatsCard
            icon={<TrendingUp className="w-6 h-6" />}
            label="AI-Focused"
            value={stats?.ai_investors || 0}
            color="purple"
          />
          <StatsCard
            icon={<Users className="w-6 h-6" />}
            label="Fintech"
            value={stats?.fintech_investors || 0}
            color="green"
          />
          <StatsCard
            icon={<Database className="w-6 h-6" />}
            label="VCs"
            value={stats?.by_type?.["Venture Capital"] || 0}
            color="orange"
          />
        </div>

        {/* Search & Filters */}
        <div className="bg-[#111] border border-gray-800 rounded-xl p-4 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            {/* Search */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search investors by name or sector..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-[#0a0a0a] border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
              />
            </div>

            {/* Type Filter */}
            <div className="flex items-center gap-2">
              <Filter className="w-5 h-5 text-gray-400" />
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="px-4 py-3 bg-[#0a0a0a] border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
              >
                <option value="">All Types</option>
                <option value="Venture Capital">Venture Capital</option>
                <option value="Family Office">Family Office</option>
                <option value="Institutional Investor">Institutional</option>
                <option value="Private Equity">Private Equity</option>
              </select>
            </div>

            {/* Focus Filter */}
            <select
              value={filterFocus}
              onChange={(e) => setFilterFocus(e.target.value)}
              className="px-4 py-3 bg-[#0a0a0a] border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
            >
              <option value="">All Focus</option>
              <option value="ai">AI/ML</option>
              <option value="fintech">Fintech</option>
              <option value="music">Music Tech</option>
            </select>
          </div>
        </div>

        {/* Results */}
        <div className="mb-4 text-gray-400">
          Showing {filteredInvestors.length} of {investors.length} investors
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : filteredInvestors.length === 0 ? (
          <div className="text-center py-20 text-gray-400">
            <Database className="w-16 h-16 mx-auto mb-4 opacity-50" />
            <p className="text-xl">No investors found</p>
            <p className="text-sm mt-2">Try adjusting your search or filters</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredInvestors.map((investor) => (
              <InvestorCard key={investor.id} investor={investor} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
