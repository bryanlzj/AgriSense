import * as React from "react";

import { cn } from "@/lib/utils";

export interface SmartMenuProps extends React.HTMLAttributes<HTMLDivElement> {
  mode?: "classic" | "smart";
  onModeChange?: (mode: "classic" | "smart") => void;
  quickActions?: Array<{
    id: string;
    icon: string;
    title: string;
    isPrimary?: boolean;
    onClick?: () => void;
  }>;
  searchPlaceholder?: string;
  onSearch?: (query: string) => void;
  readonly recentItems?: ReadonlyArray<{
    readonly id: string;
    readonly name: string;
    readonly initials: string;
    readonly onClick?: () => void;
  }>;
  navigationItems?: Array<{
    id: string;
    icon: string;
    label: string;
    isActive?: boolean;
    badge?: number;
    onClick?: () => void;
  }>;
}

export function SmartMenu({
  className,
  mode = "smart",
  onModeChange,
  quickActions = [
    { id: "profile", icon: "◉", title: "View Customer Profile" },
    { id: "report", icon: "◈", title: "Generate Report" },
    { id: "meeting", icon: "◐", title: "Schedule Meeting" },
  ],
  searchPlaceholder = "Search customers",
  onSearch,
  recentItems = [
    { id: "1", name: "AuthorityHub Ltd", initials: "A" },
    { id: "2", name: "MidwestParts Inc", initials: "M" },
    { id: "3", name: "Precision Systems", initials: "P" },
  ],
  navigationItems = [
    {
      id: "dashboard",
      icon: "◦",
      label: "Performance Dashboard",
      isActive: true,
    },
    { id: "orders", icon: "◦", label: "Order History" },
    { id: "financial", icon: "◦", label: "Financial Analysis" },
    { id: "analytics", icon: "◦", label: "Product Analytics" },
    { id: "timeline", icon: "◦", label: "Activity Timeline" },
    { id: "risk", icon: "◦", label: "Risk Management" },
  ],
  ...props
}: Readonly<SmartMenuProps>) {
  const [currentMode, setCurrentMode] = React.useState(mode);
  const [searchQuery, setSearchQuery] = React.useState("");

  const handleModeChange = (newMode: "classic" | "smart") => {
    setCurrentMode(newMode);
    onModeChange?.(newMode);
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);
    onSearch?.(query);
  };

  return (
    <div
      className={cn("bg-white border border-gray-200 rounded-xl shadow-lg w-64 h-fit overflow-hidden", className)}
      {...props}
    >
      {/* iOS-style Toggle Header */}
      <div className="p-3 border-b border-gray-200">
        <div className="flex items-center justify-center gap-2">
          <span className="text-sm text-muted-foreground">Classic</span>
          <button
            onClick={() => handleModeChange(currentMode === "smart" ? "classic" : "smart")}
            className={cn(
              "relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2",
              currentMode === "smart" ? "bg-teal-500" : "bg-muted",
            )}
          >
            <span
              className={cn(
                "inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200 ease-in-out",
                currentMode === "smart" ? "translate-x-6" : "translate-x-1",
              )}
            />
          </button>
          <span className="text-sm text-muted-foreground">Smart</span>
        </div>
      </div>

      {currentMode === "smart" ? (
        <>
          {/* Smart Mode Content */}
          <div className="p-3 space-y-3">
            {/* Quick Actions */}
            <div className="space-y-1">
              {quickActions.map((action) => (
                <button
                  key={action.id}
                  onClick={action.onClick}
                  className="w-full flex items-center gap-2 p-2 text-left text-sm hover:bg-muted/50 transition-colors rounded-md"
                >
                  <span className="text-base">{action.icon}</span>
                  <span className="text-foreground">{action.title}</span>
                </button>
              ))}
            </div>

            {/* Search Input */}
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={handleSearchChange}
                placeholder={searchPlaceholder}
                className="w-full px-3 py-2 bg-muted/50 rounded-md border-0 focus:ring-1 focus:ring-primary/50 focus:bg-background transition-colors text-sm"
              />
              <div className="absolute right-2 top-1/2 transform -translate-y-1/2 text-muted-foreground text-sm">⌕</div>
            </div>

            {/* Recent Items */}
            <div>
              <h3 className="text-xs text-muted-foreground mb-1 uppercase tracking-wide font-normal">
                Recent Customers
              </h3>
              <div className="space-y-0.5">
                {recentItems.map((item) => (
                  <button
                    key={item.id}
                    onClick={item.onClick}
                    className="w-full flex items-center gap-2 p-1.5 hover:bg-muted/50 transition-colors text-left rounded-md"
                  >
                    <div className="w-6 h-6 bg-teal-500 text-white rounded-full flex items-center justify-center text-xs font-medium">
                      {item.initials}
                    </div>
                    <span className="text-sm text-foreground">{item.name}</span>
                    <span className="ml-auto text-muted-foreground">›</span>
                  </button>
                ))}
                <button className="w-full text-left p-1.5 text-sm text-teal-600 hover:bg-muted/50 transition-colors rounded-md">
                  View all customers
                </button>
              </div>
            </div>
          </div>

          {/* Navigation in Smart Mode */}
          <div className="px-3 pb-3">
            <nav className="space-y-0.5">
              {navigationItems.map((item) => (
                <button
                  key={item.id}
                  onClick={item.onClick}
                  className={cn(
                    "w-full flex items-center gap-2 px-2 py-1.5 text-left text-sm transition-colors rounded-md",
                    item.isActive ? "bg-teal-500/10 text-teal-700 font-medium" : "hover:bg-muted/50 text-foreground",
                  )}
                >
                  <span className="text-base">{item.icon}</span>
                  <span>{item.label}</span>
                  {item.badge && (
                    <span className="ml-auto bg-destructive text-destructive-foreground text-xs px-1.5 py-0.5 rounded-full min-w-[16px] text-center">
                      {item.badge}
                    </span>
                  )}
                </button>
              ))}
            </nav>
          </div>
        </>
      ) : (
        <>
          {/* Classic Mode Content */}
          <nav className="p-3 space-y-0.5">
            {navigationItems.map((item) => (
              <button
                key={item.id}
                onClick={item.onClick}
                className={cn(
                  "w-full flex items-center gap-2 px-2 py-1.5 text-left text-sm transition-colors rounded-md",
                  item.isActive ? "bg-primary/10 text-primary font-medium" : "hover:bg-muted/50 text-foreground",
                )}
              >
                <span className="text-base">{item.icon}</span>
                <span>{item.label}</span>
                {item.badge && (
                  <span className="ml-auto bg-destructive text-destructive-foreground text-xs px-1.5 py-0.5 rounded-full min-w-[16px] text-center">
                    {item.badge}
                  </span>
                )}
              </button>
            ))}
          </nav>
        </>
      )}
    </div>
  );
}
