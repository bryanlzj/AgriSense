import * as React from "react";
import { Info } from "lucide-react";

import { cn } from "@/lib/utils";

export interface StatsCirclesProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  stats?: Array<{
    value: number;
    label: string;
    color?: string;
  }>;
}

export function StatsCircles({
  className,
  title = "Workforce readiness",
  stats = [
    { value: 68.4, label: "Availability", color: "#10B981" },
    { value: 72.1, label: "Engagement", color: "#8B5CF6" },
    { value: 81.3, label: "Skills", color: "#F59E0B" },
    { value: 64.8, label: "Payroll", color: "#10B981" },
  ],
  ...props
}: Readonly<StatsCirclesProps>) {
  return (
    <div className={cn("bg-card rounded-2xl p-7 border shadow-sm", className)} {...props}>
      <div className="flex justify-between items-center mb-7">
        <h3 className="text-xl font-semibold text-foreground">{title}</h3>
        <div className="w-6 h-6 rounded-full bg-muted flex items-center justify-center text-muted-foreground cursor-pointer hover:bg-secondary hover:text-foreground transition-all">
          <Info size={14} />
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
        {stats.map((stat) => {
          const circumference = 2 * Math.PI * 40;
          const strokeDashoffset = circumference - (stat.value / 100) * circumference;

          return (
            <div key={stat.label} className="text-center">
              <div className="relative w-24 h-24 mx-auto mb-3">
                <svg className="w-full h-full transform -rotate-90" width="96" height="96" viewBox="0 0 96 96">
                  {/* Background circle */}
                  <circle cx="48" cy="48" r="40" fill="none" stroke="hsl(var(--border))" strokeWidth="8" />
                  {/* Progress circle */}
                  <circle
                    cx="48"
                    cy="48"
                    r="40"
                    fill="none"
                    stroke={stat.color}
                    strokeWidth="8"
                    strokeDasharray={circumference}
                    strokeDashoffset={strokeDashoffset}
                    strokeLinecap="round"
                    className="transition-all duration-1000 ease-out"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-lg font-bold text-foreground">{stat.value}%</span>
                </div>
              </div>
              <div className="text-sm font-medium text-muted-foreground">{stat.label}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
