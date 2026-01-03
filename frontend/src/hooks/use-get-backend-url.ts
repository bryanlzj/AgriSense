import { useState } from "react";

const getInitialBackendUrl = (): string => {
  if (typeof window !== "undefined") {
    const hostname = window.location.hostname;

    if (hostname.includes(".e2b.app")) {
      const match = hostname.match(/(\d+)-(.+)\.e2b\.app/);

      if (match) {
        const [, , instanceId] = match;
        return `https://5000-${instanceId}.e2b.app`;
      }
    }
  }
  return "http://localhost:5000";
};

export const useGetBackendUrl = () => {
  const [backendUrl] = useState<string>(getInitialBackendUrl);
  return backendUrl;
};
