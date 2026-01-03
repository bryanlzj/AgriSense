import * as React from "react";

import { cn } from "@/lib/utils";

export interface TaskCardsProps extends React.HTMLAttributes<HTMLElement> {
  tasks?: Array<{
    id: string;
    title: string;
    description?: string;
    assignees: Array<{
      name: string;
      initials: string;
      avatar?: string;
    }>;
    status: "pending" | "in-progress" | "completed";
    priority?: "low" | "medium" | "high";
    dueDate?: string;
  }>;
}

export function TaskCards({
  className,
  tasks = [
    {
      id: "1",
      title: "Review customer applications",
      description: "Process 12 pending customer applications before deadline",
      assignees: [
        { name: "John Doe", initials: "JD" },
        { name: "Alice Smith", initials: "AS" },
        { name: "Mike Johnson", initials: "MJ" },
      ],
      status: "pending",
      priority: "high",
      dueDate: "Today",
    },
    {
      id: "2",
      title: "Update project documentation",
      description: "Refresh API docs and user guides",
      assignees: [
        { name: "Sarah Wilson", initials: "SW" },
        { name: "David Brown", initials: "DB" },
      ],
      status: "in-progress",
      priority: "medium",
      dueDate: "Tomorrow",
    },
    {
      id: "3",
      title: "Quarterly team review",
      description: "Conduct performance reviews for Q1",
      assignees: [{ name: "Lisa Davis", initials: "LD" }],
      status: "completed",
      priority: "low",
      dueDate: "Last week",
    },
  ],
  ...props
}: Readonly<TaskCardsProps>) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "text-green-600 bg-green-100";
      case "in-progress":
        return "text-blue-600 bg-blue-100";
      default:
        return "text-orange-600 bg-orange-100";
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high":
        return "border-l-red-500";
      case "medium":
        return "border-l-yellow-500";
      default:
        return "border-l-green-500";
    }
  };

  return (
    <section className={cn("py-8 px-4 bg-background", className)} {...props}>
      <div className="container mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tasks.map((task) => (
            <div
              key={task.id}
              className={cn(
                "bg-card rounded-lg p-6 border-l-4 border shadow-sm hover:shadow-md transition-all duration-200 cursor-pointer group",
                getPriorityColor(task.priority ?? "low"),
              )}
            >
              {/* Task assignees */}
              <div className="flex items-center mb-4 -space-x-2">
                {task.assignees.slice(0, 3).map((assignee) => (
                  <div
                    key={assignee.name}
                    className="w-8 h-8 rounded-lg bg-primary text-primary-foreground border-2 border-background flex items-center justify-center text-xs font-semibold transition-transform group-hover:scale-105"
                    title={assignee.name}
                  >
                    {assignee.avatar ? (
                      <img
                        src={assignee.avatar}
                        alt={assignee.name}
                        className="w-full h-full rounded-lg object-cover"
                      />
                    ) : (
                      assignee.initials
                    )}
                  </div>
                ))}
                {task.assignees.length > 3 && (
                  <div className="w-8 h-8 rounded-lg bg-muted text-muted-foreground border-2 border-background flex items-center justify-center text-xs font-semibold">
                    +{task.assignees.length - 3}
                  </div>
                )}
              </div>

              {/* Task content */}
              <div className="space-y-3 flex-1">
                <h3 className="font-semibold text-foreground leading-tight group-hover:text-primary transition-colors">
                  {task.title}
                </h3>

                {task.description && (
                  <p className="text-sm text-muted-foreground leading-relaxed">{task.description}</p>
                )}

                {/* Task meta */}
                <div className="flex items-center justify-between pt-2">
                  <div className="flex items-center gap-2">
                    <span
                      className={cn(
                        "px-2 py-1 rounded-full text-xs font-medium capitalize",
                        getStatusColor(task.status),
                      )}
                    >
                      {task.status.replace("-", " ")}
                    </span>
                  </div>

                  {task.dueDate && <span className="text-xs text-muted-foreground">📅 {task.dueDate}</span>}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
