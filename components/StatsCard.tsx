import { ReactNode } from "react";

interface StatsCardProps {
  icon: ReactNode;
  label: string;
  value: number | string;
  color: "blue" | "purple" | "green" | "orange";
}

export default function StatsCard({ icon, label, value, color }: StatsCardProps) {
  const colorClasses = {
    blue: "bg-blue-500/10 border-blue-500/20 text-blue-400",
    purple: "bg-purple-500/10 border-purple-500/20 text-purple-400",
    green: "bg-green-500/10 border-green-500/20 text-green-400",
    orange: "bg-orange-500/10 border-orange-500/20 text-orange-400",
  };

  const iconBg = {
    blue: "bg-blue-500/20",
    purple: "bg-purple-500/20",
    green: "bg-green-500/20",
    orange: "bg-orange-500/20",
  };

  return (
    <div className={`rounded-xl border p-5 ${colorClasses[color]}`}>
      <div className="flex items-center gap-4">
        <div className={`p-3 rounded-lg ${iconBg[color]}`}>{icon}</div>
        <div>
          <p className="text-sm text-gray-400">{label}</p>
          <p className="text-2xl font-bold text-white">{value.toLocaleString()}</p>
        </div>
      </div>
    </div>
  );
}
