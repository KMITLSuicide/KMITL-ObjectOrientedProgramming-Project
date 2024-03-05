"use client";

import { useEffect, useState } from "react";
import * as React from "react";
import { Check, ChevronsUpDown } from "lucide-react";

import {
  type CategoryData,
  getCategoryDataFromAPI,
} from "~/src/lib/data/category";
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

export default function CategoryChoosePage() {
  const [categoryData, setCategoryData] = useState<
    CategoryData[] | null | undefined
  >(undefined);
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState("");
  const router = useRouter();

  useEffect(() => {
    async function fetchData() {
      const apiData = await getCategoryDataFromAPI();
      console.log(apiData);
      setCategoryData(apiData);
    }
    void fetchData();
  }, []);

  return (
    <div className="flex h-full flex-col items-center justify-center">
      <div className="flex space-y-4 flex-col items-center justify-center bg-secondary p-8 rounded-lg">
        <h1 className="text-2xl font-bold text-center">Select a category</h1>
        <Popover open={open} onOpenChange={setOpen}>
          <PopoverTrigger asChild>
            <Button
              variant="outline"
              role="combobox"
              aria-expanded={open}
              className="w-[200px] justify-between hover:bg-background"
            >
              {value
                ? categoryData?.find((category) => category._CourseCategory__name.toLowerCase() === value)?._CourseCategory__name
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
                    key={category._CourseCategory__id}
                    value={category._CourseCategory__name}
                    onSelect={(currentValue) => {
                      setValue(currentValue === value ? "" : currentValue);
                      setOpen(false);
                      router.push(`/category/${category._CourseCategory__id}`);
                    }}
                  >
                    <Check
                      className={cn(
                        "mr-2 h-4 w-4",
                        value === category._CourseCategory__name ? "opacity-100" : "opacity-0",
                      )}
                    />
                    {category._CourseCategory__name}
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
