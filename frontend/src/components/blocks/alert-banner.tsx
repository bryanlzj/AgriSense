import * as React from "react";
import { AlertTriangle, Check, CircleX, Info, X } from "lucide-react";

import { cn } from "@/lib/utils";

export interface AlertBannerProps extends React.HTMLAttributes<HTMLDivElement> {
  title: string;
  description?: string;
  variant?: "info" | "warning" | "error" | "success";
  actionText?: string;
  onAction?: () => void;
  onDismiss?: () => void;
  dismissible?: boolean;
}

export function AlertBanner({
  className,
  title,
  description,
  variant = "info",
  actionText,
  onAction,
  onDismiss,
  dismissible = true,
  ...props
}: Readonly<AlertBannerProps>) {
  const [isVisible, setIsVisible] = React.useState(true);

  const handleDismiss = () => {
    setIsVisible(false);
    onDismiss?.();
  };

  const getVariantStyles = () => {
    switch (variant) {
      case "error":
        return {
          container: "bg-destructive/10 border-destructive/20 text-foreground",
          icon: "text-destructive",
          button: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        };
      case "warning":
        return {
          container: "bg-warning/10 border-warning/20 text-foreground",
          icon: "text-warning",
          button: "bg-warning text-warning-foreground hover:bg-warning/90",
        };
      case "success":
        return {
          container: "bg-success/10 border-success/20 text-foreground",
          icon: "text-success",
          button: "bg-success text-success-foreground hover:bg-success/90",
        };
      default:
        return {
          container: "bg-info/10 border-info/20 text-foreground",
          icon: "text-info",
          button: "bg-info text-info-foreground hover:bg-info/90",
        };
    }
  };

  const getIcon = () => {
    switch (variant) {
      case "error":
        return <CircleX className="w-5 h-5" />;
      case "warning":
        return <AlertTriangle className="w-5 h-5" />;
      case "success":
        return <Check className="w-5 h-5" />;
      default:
        return <Info className="w-5 h-5" />;
    }
  };

  const styles = getVariantStyles();

  if (!isVisible) return null;

  return (
    <div className={cn("relative overflow-hidden rounded-lg border p-4", styles.container, className)} {...props}>
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-3 flex-1">
          <div className={cn("mt-0.5", styles.icon)}>{getIcon()}</div>
          <div className="space-y-1">
            <h4 className="font-medium">{title}</h4>
            {description && <p className="text-sm text-muted-foreground">{description}</p>}
          </div>
        </div>

        <div className="flex items-center gap-2">
          {actionText && onAction && (
            <button
              onClick={onAction}
              className={cn(
                "inline-flex items-center justify-center rounded-md px-3 py-1.5 text-xs font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring",
                styles.button,
              )}
            >
              {actionText}
            </button>
          )}

          {dismissible && (
            <button
              onClick={handleDismiss}
              className="inline-flex items-center justify-center w-6 h-6 rounded-md text-muted-foreground hover:text-foreground transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
