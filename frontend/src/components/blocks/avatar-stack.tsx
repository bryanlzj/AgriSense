import * as React from "react";

import { cn } from "@/lib/utils";

export interface AvatarStackProps extends React.HTMLAttributes<HTMLDivElement> {
  avatars?: Array<{
    name: string;
    initials?: string;
    image?: string;
    color?: string;
  }>;
  maxVisible?: number;
  size?: "sm" | "md" | "lg";
  spacing?: "tight" | "normal" | "loose";
  showTooltip?: boolean;
}

export function AvatarStack({
  className,
  avatars = [
    { name: "John Doe", initials: "JD", color: "bg-blue-500" },
    { name: "Alice Smith", initials: "AS", color: "bg-purple-500" },
    { name: "Mike Johnson", initials: "MJ", color: "bg-green-500" },
    { name: "Sarah Wilson", initials: "SW", color: "bg-yellow-500" },
  ],
  maxVisible = 4,
  size = "md",
  spacing = "normal",
  showTooltip = true,
  ...props
}: Readonly<AvatarStackProps>) {
  const visibleAvatars = avatars.slice(0, maxVisible);
  const remainingCount = Math.max(0, avatars.length - maxVisible);

  const sizeClasses = {
    sm: "w-8 h-8 text-xs",
    md: "w-10 h-10 text-sm",
    lg: "w-12 h-12 text-base",
  };

  const spacingClasses = {
    tight: "-space-x-1",
    normal: "-space-x-2",
    loose: "space-x-1",
  };

  return (
    <div className={cn("flex items-center", spacingClasses[spacing], className)} {...props}>
      {visibleAvatars.map((avatar, index) => (
        <div
          key={`${avatar.name}-${index}`}
          className={cn(
            "relative flex items-center justify-center rounded-full border-2 border-background font-semibold text-white transition-all duration-200 hover:scale-110 hover:z-10 cursor-pointer",
            sizeClasses[size],
            avatar.color ?? "bg-primary",
          )}
          style={{
            zIndex: visibleAvatars.length - index,
          }}
          title={showTooltip ? avatar.name : undefined}
        >
          {avatar.image ? (
            <img src={avatar.image} alt={avatar.name} className="w-full h-full rounded-full object-cover" />
          ) : (
            <span>{avatar.initials ?? avatar.name.charAt(0).toUpperCase()}</span>
          )}
        </div>
      ))}

      {/* Overflow indicator */}
      {remainingCount > 0 && (
        <div
          className={cn(
            "relative flex items-center justify-center rounded-full border-2 border-background bg-muted text-muted-foreground font-semibold transition-all duration-200 hover:scale-110 hover:z-10 cursor-pointer",
            sizeClasses[size],
          )}
          style={{ zIndex: 0 }}
          title={showTooltip ? `+${remainingCount} more` : undefined}
        >
          <span>+{remainingCount}</span>
        </div>
      )}
    </div>
  );
}
