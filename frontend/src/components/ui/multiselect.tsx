import React, { useState } from "react";
import { ChevronsUpDown } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
import { Checkbox } from "@/components/ui/checkbox";
import { cn } from "@/lib/utils";

interface Option {
  value: string;
  label: string;
}

interface MultiSelectProps {
  options?: Option[];
  placeholder?: string;
  emptyMessage?: string;
  maxDisplay?: number;
  value?: string[];
  onValueChange?: (value: string[]) => void;
}

export const MultiSelect: React.FC<MultiSelectProps> = ({
  options = [],
  placeholder = "Select items...",
  emptyMessage = "No items found.",
  maxDisplay = 3,
  value,
  onValueChange,
}) => {
  const [open, setOpen] = useState<boolean>(false);
  const [internalValue, setInternalValue] = useState<string[]>([]);
  const [searchValue, setSearchValue] = useState<string>("");

  // Use controlled or uncontrolled state
  const isControlled = value !== undefined;
  const selectedValues = isControlled ? value : internalValue;
  const setSelectedValues = isControlled ? onValueChange! : setInternalValue;

  const handleSelect = (optionValue: string) => {
    const newValues = selectedValues.includes(optionValue)
      ? selectedValues.filter((item) => item !== optionValue)
      : [...selectedValues, optionValue];

    setSelectedValues(newValues);
  };

  const handleRemove = (optionValue: string) => {
    const newValues = selectedValues.filter((item) => item !== optionValue);
    setSelectedValues(newValues);
  };

  const clearAll = () => {
    setSelectedValues([]);
  };

  const selectedItems = options.filter((option) => selectedValues.includes(option.value));
  const displayItems = selectedItems.slice(0, maxDisplay);
  const remainingCount = selectedItems.length - maxDisplay;

  return (
    <div className="w-full">
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <div
            role="button"
            className={cn(
              "border-input w-full flex items-center justify-between min-h-10 h-auto py-2 px-3 text-sm",
              "border rounded-md bg-background cursor-pointer",
              "hover:bg-accent hover:text-accent-foreground",
              "focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
              "disabled:cursor-not-allowed disabled:opacity-50",
            )}
            onClick={() => setOpen(!open)}
          >
            <div className="flex flex-wrap items-center gap-1 flex-1 min-w-0 pr-2">
              {selectedValues.length === 0 ? (
                <span className="text-muted-foreground">{placeholder}</span>
              ) : (
                <>
                  {displayItems.map((item) => (
                    <div key={item.value} onClick={(e) => e.stopPropagation()}>
                      <Badge variant="secondary" onClose={() => handleRemove(item.value)}>
                        {item.label}
                      </Badge>
                    </div>
                  ))}
                  {remainingCount > 0 && <Badge variant="outline">+{remainingCount} more</Badge>}
                </>
              )}
            </div>
            <ChevronsUpDown className="h-4 w-4 shrink-0 opacity-50" />
          </div>
        </PopoverTrigger>
        <PopoverContent className="w-full p-0" align="start">
          <Command>
            <CommandInput placeholder="Search items..." value={searchValue} onValueChange={setSearchValue} />
            <CommandList>
              <CommandEmpty>{emptyMessage}</CommandEmpty>
              <CommandGroup>
                {selectedValues.length > 0 && (
                  <CommandItem onSelect={clearAll} className="justify-center text-center">
                    Clear all ({selectedValues.length})
                  </CommandItem>
                )}
                {options.map((option) => {
                  const isSelected = selectedValues.includes(option.value);
                  return (
                    <CommandItem key={option.value} value={option.label} onSelect={() => handleSelect(option.value)}>
                      <Checkbox checked={isSelected} className="mr-2" />
                      <span>{option.label}</span>
                    </CommandItem>
                  );
                })}
              </CommandGroup>
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  );
};
