"use client";

import { useState } from "react";
import * as React from "react";
import { Check, ChevronsUpDown } from "lucide-react";

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

const categoryData = [
  {
    name: "Video",
    link: "new/video"
  },
  {
    name: "Image",
    link: "new/image"
  },
  {
    name: "Quiz",
    link: "new/quiz"
  },
];

export default function CategoryChoosePage() {
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState("");
  const router = useRouter();

  return (
    <div className="flex h-full flex-col">
      <h1 className="text-2xl font-bold">Select material type</h1>
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
              : "Select material type..."}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[200px] p-0">
          <Command>
            <CommandInput placeholder="Search material type..." />
            <CommandEmpty>No material type found.</CommandEmpty>
            <CommandGroup>
              {categoryData?.map((category) => (
                <CommandItem
                  key={category.name}
                  value={category.name}
                  onSelect={(currentValue) => {
                    setValue(currentValue === value ? "" : currentValue);
                    setOpen(false);
                    router.replace(category.link);
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
);
}
