import { useQuery } from "@tanstack/react-query";

/**
 * Example query hook demonstrating Tanstack Query usage
 *
 * Replace this with your actual API calls
 */
export function useExampleQuery() {
  return useQuery({
    queryKey: ["example"],
    queryFn: async () => {
      // Replace with your actual API endpoint
      const response = await fetch("https://api.example.com/data");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    },
    // Optional: configure behavior
    enabled: true, // Set to false to disable automatic fetching
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchOnWindowFocus: false,
  });
}
