"use client";

import { Building2, MapPin, DollarSign, Target, ExternalLink, Users } from "lucide-react";

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

interface InvestorCardProps {
  investor: Investor;
}

export default function InvestorCard({ investor }: InvestorCardProps) {
  const typeColors: Record<string, string> = {
    "Venture Capital": "bg-blue-500/20 text-blue-400 border-blue-500/30",
    "Family Office": "bg-purple-500/20 text-purple-400 border-purple-500/30",
    "Institutional Investor": "bg-green-500/20 text-green-400 border-green-500/30",
    "Private Equity": "bg-orange-500/20 text-orange-400 border-orange-500/30",
  };

  const sectors = investor.sectors?.split(",").slice(0, 3) || [];

  return (
    <div className="bg-[#111] border border-gray-800 rounded-xl p-5 hover:border-gray-700 transition-all hover:shadow-lg hover:shadow-blue-500/5">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
            <Building2 className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-white text-lg leading-tight">{investor.name}</h3>
            <span
              className={`inline-block px-2 py-0.5 text-xs rounded-full border ${
                typeColors[investor.type] || "bg-gray-500/20 text-gray-400 border-gray-500/30"
              }`}
            >
              {investor.type}
            </span>
          </div>
        </div>
        {investor.website && (
          <a
            href={investor.website}
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-400 hover:text-blue-400 transition-colors"
          >
            <ExternalLink className="w-4 h-4" />
          </a>
        )}
      </div>

      {/* Info */}
      <div className="space-y-3 mb-4">
        {investor.aum_estimate && (
          <div className="flex items-center gap-2 text-sm">
            <DollarSign className="w-4 h-4 text-green-400" />
            <span className="text-gray-300">AUM: {investor.aum_estimate}</span>
          </div>
        )}

        {investor.state && (
          <div className="flex items-center gap-2 text-sm">
            <MapPin className="w-4 h-4 text-blue-400" />
            <span className="text-gray-300">{investor.state}</span>
          </div>
        )}

        {investor.investment_focus && (
          <div className="flex items-start gap-2 text-sm">
            <Target className="w-4 h-4 text-purple-400 mt-0.5" />
            <span className="text-gray-300 line-clamp-2">{investor.investment_focus}</span>
          </div>
        )}

        {investor.decision_makers && (
          <div className="flex items-start gap-2 text-sm">
            <Users className="w-4 h-4 text-orange-400 mt-0.5" />
            <span className="text-gray-400 line-clamp-1">{investor.decision_makers}</span>
          </div>
        )}
      </div>

      {/* Sectors */}
      {sectors.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {sectors.map((sector, i) => (
            <span
              key={i}
              className="px-2 py-1 text-xs bg-gray-800 text-gray-300 rounded-md"
            >
              {sector.trim()}
            </span>
          ))}
        </div>
      )}

      {/* Notable Investments */}
      {investor.notable_investments && (
        <div className="mt-4 pt-4 border-t border-gray-800">
          <p className="text-xs text-gray-500 mb-1">Notable Investments</p>
          <p className="text-sm text-gray-400 line-clamp-2">{investor.notable_investments}</p>
        </div>
      )}
    </div>
  );
}
