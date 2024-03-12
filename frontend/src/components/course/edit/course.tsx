import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useForm, useWatch } from "react-hook-form";
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
import type { CourseInfo } from "~/src/lib/definitions/course";
import { Check, ChevronsUpDown } from "lucide-react";
import { cn } from "~/src/lib/utils";
import { deleteCourse, editCourseInfo } from "~/src/lib/data/course-edit";

const FormSchema = z.object({
  name: z.string().min(1),
  description: z.string().min(1),
  price: z.coerce.number().int().positive(),
  category_id: z.string().uuid(),
});

export function CourseEdit({
  courseInfo
} : {
  courseInfo: CourseInfo
}) {
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
    setValue(courseInfo.category_name);
  }, [courseInfo.category_name]);

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      name: courseInfo?.name,
      description: courseInfo?.description,
      price: courseInfo?.price,
      category_id: courseInfo.category_id
    },
  });

  const watchedFields = useWatch({ control: form.control });

  async function onDeleteCourse() {
    const response = await deleteCourse(courseInfo.id);
    if (response === false) {
      toast({
        title: "Error",
        description: "Failed to delete course",
        variant: "destructive",
      });
    } else {
      toast({
        title: "Success",
        description: "Course deleted",
      });
      router.push("/account/teaching");
    }
  }

  function onSubmit(data: z.infer<typeof FormSchema>) {
    void editCourseInfo(courseInfo.id, data).then((response) => {
      if (response === false) {
      toast({
        title: "Error",
        description: "Failed to update course",
        variant: "destructive",
      });
    } else {
      toast({
        title: "Success",
        description: "Course updated",
      });
      router.refresh();
    }});
  }

  return (
    <>
      <div>
        <h1 className="text-2xl font-bold">Preview</h1>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={courseInfo.banner_image}
          alt={watchedFields?.description ?? "description not found"}
          height={320}
          style={{
            objectFit: "contain",
            width: "100%",
            height: "320px",
          }}
        />
        <h2 className="text-4xl font-bold">{watchedFields?.name}</h2>
        <p className="text-lg">{watchedFields?.description}</p>
      </div>
      <div>
        <hr className="my-4 h-px border-0 bg-muted-foreground" />
      </div>
      <div>
        <h1 className="text-2xl font-bold">Edit</h1>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="w-full space-y-4"
          >
            <div className="space-y-2">
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Name</FormLabel>
                    <FormControl>
                      <Input {...field} />
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
                      <Input {...field} />
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
                      <Input {...field} type="number" />
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
                          size={16}
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
            </div>
            <Button type="submit" className="my-8">
              Save
            </Button>
          </form>
        </Form>

        <Button variant="destructive" onClick={onDeleteCourse} className="mt-6">
          Delete Course
        </Button>
      </div>
    </>
  );
}