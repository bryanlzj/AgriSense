import { Button } from "@/components/ui/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { ThemeToggle } from "@/components/ui/theme-toggle";
import evobuilderLogo from "/evo-builder-logo.png";

export default function App() {
  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <img src={evobuilderLogo} alt="Evo Builder" width={100} height={100} />
        <h1 className="text-4xl font-bold">Welcome to the Evo Template</h1>
        <p>Start building by prompting in the chat.</p>
        <div className="flex items-center gap-4">
          <Popover>
            <PopoverTrigger asChild>
              <Button>Start</Button>
            </PopoverTrigger>
            <PopoverContent>
              <p>You really thought you could start building without a prompt? Use the chat to get started 😉</p>
            </PopoverContent>
          </Popover>
          <ThemeToggle />
        </div>
      </main>
    </div>
  );
}
