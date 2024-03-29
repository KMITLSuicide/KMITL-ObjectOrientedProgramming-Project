"use client";

import { useEffect, useState } from "react";
import * as React from "react";
import { Check, ChevronsUpDown } from "lucide-react";

import { getCategoryNamesFromAPI } from "~/src/lib/data/category";
import { cn } from "~/src/lib/utils";
import { Button } from "~/src/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from "~/src/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "~/src/components/ui/popover";
import { useRouter } from "next/navigation";
import { type CategoryNames } from "~/src/lib/definitions/category";
import { toast } from "~/src/components/ui/use-toast";

export default function CategoryChoosePage() {
  const [categoryData, setCategoryData] = useState<
    CategoryNames[] | null | undefined
  >(undefined);
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState("");
  const router = useRouter();

  useEffect(() => {
    async function fetchData() {
      const apiData = await getCategoryNamesFromAPI();
      setCategoryData(apiData);
      if (apiData === null) {
        toast({
          title: "Error",
          description: "Failed to fetch category data",
          variant: "destructive",
        })}
    }
    void fetchData();
  }, []);

  return (
    <div className="flex h-full flex-col items-center justify-center">
      <div className="flex flex-col items-center justify-center space-y-4 rounded-lg bg-secondary p-8">
        <h1 className="text-center text-2xl font-bold">Select a category</h1>
        <Popover open={open} onOpenChange={setOpen}>
          <PopoverTrigger asChild>
            <Button
              variant="outline"
              role="combobox"
              aria-expanded={open}
              className="w-[200px] justify-between hover:bg-background"
            >
              {value
                ? categoryData?.find(
                    (category) => category.name.toLowerCase() === value,
                  )?.name
                : "Select category..."}
              <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-[200px] p-0">
            <Command>
              <CommandInput placeholder="Search category..." />
              <CommandEmpty>No category found.</CommandEmpty>
              <CommandGroup>
                {categoryData?.map((category) => (
                  <CommandItem
                    key={category.id}
                    value={category.name}
                    onSelect={(currentValue) => {
                      setValue(currentValue === value ? "" : currentValue);
                      setOpen(false);
                      router.push(`/category/${category.id}`);
                    }}
                >
                  <Check
                    className={cn(
                      "mr-2 h-4 w-4",
                      value === category.name ? "opacity-100" : "opacity-0",
                    )}
                  />
                  {category.name}
                </CommandItem>
              ))}
            </CommandGroup>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  </div>
);
}
