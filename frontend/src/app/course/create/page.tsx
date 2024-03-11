"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "~/src/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "~/src/components/ui/form";
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
import { Input } from "~/src/components/ui/input";
import { toast } from "~/src/components/ui/use-toast";
import { getCategoryNamesFromAPI } from "~/src/lib/data/category";
import type { CategoryNames } from "~/src/lib/definitions/category";
import { Check, ChevronsUpDown } from "lucide-react";
import { cn } from "~/src/lib/utils";
import { createCourseToAPI } from "~/src/lib/data/course-create";
import { useRouter } from "next/navigation";

const FormSchema = z.object({
  name: z.string().min(1),
  description: z.string().min(1),
  price: z.coerce.number().int().positive(),
  category_id: z.string().uuid(),
});

export default function CreateCourse() {
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
        });
      }
    }
    void fetchData();
  }, []);

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
  });

  function onSubmit(data: z.infer<typeof FormSchema>) {
    // toast({
    //   title: "You submitted the following values:",
    //   description: (
    //     <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
    //       <code className="text-white">{JSON.stringify(data, null, 2)}</code>
    //     </pre>
    //   ),
    // });

    void createCourseToAPI(data).then((response) => {
      if (response === null) {
        toast({
          title: "Error",
          description: "Failed to create course",
          variant: "destructive",
        });
      } else {
        toast({
          title: "Success",
          description: "Course created",
          variant: "default",
        });

        router.push(`/course/${response.id}/edit`);
      }
    });
  }

  return (
    <div className="flex h-full w-full items-center justify-center">
      <div className="bg-muted p-8 rounded-lg">
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="w-full space-y-6"
          >
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Name</FormLabel>
                  <FormControl>
                    <Input placeholder="Python" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Description</FormLabel>
                  <FormControl>
                    <Input placeholder="Python basics" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="price"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Price</FormLabel>
                  <FormControl>
                    <Input placeholder="1000" {...field} type="number" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormItem className="flex flex-col">
              <FormLabel>Category</FormLabel>
              <Popover open={open} onOpenChange={setOpen}>
                <PopoverTrigger asChild>
                  <FormControl>
                    <Button
                      variant="outline"
                      role="combobox"
                      aria-expanded={open}
                      className="w-full justify-between hover:bg-background"
                    >
                       {value
                        ? categoryData?.find(
                            (category) => category.name.toLowerCase() === value.toLowerCase(),
                          )?.name
                        : "Select category..."}
                      <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                    </Button>
                  </FormControl>
                </PopoverTrigger>
                <PopoverContent className="w-full p-0">
                  <Command>
                    <CommandInput placeholder="Search categories..." />
                    <CommandEmpty>No category found.</CommandEmpty>
                    <CommandGroup>
                      {categoryData?.map((category) => (
                        <CommandItem
                          value={category.name}
                          key={category.id}
                          onSelect={(currentValue) => {
                            console.log(category);
                            setValue(currentValue === value ? "" : currentValue);
                            form.setValue("category_id", category.id);
                            setOpen(false);
                          }}
                        >
                          <Check
                            className={cn(
                              value.toLowerCase() === category.name.toLowerCase() ? "opacity-100" : "opacity-0",
                            )}
                          />
                          {category.name}
                        </CommandItem>
                      ))}
                    </CommandGroup>
                  </Command>
                </PopoverContent>
              </Popover>
              <FormMessage />
            </FormItem>
            <Button type="submit">Create</Button>
          </form>
        </Form>
      </div>
    </div>
  );
}
