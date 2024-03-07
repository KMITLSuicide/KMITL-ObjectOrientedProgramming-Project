"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
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
import { Input } from "~/src/components/ui/input";
import { RadioGroup, RadioGroupItem } from "~/src/components/ui/radio-group";

const FormSchema = z.object({
  type: z.enum(["course", "category", "teacher"]),
  query: z.string(),
});

export default function SearchSelector() {
  const router = useRouter();
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      type: "course",
      query: "",
    },
  });

  function onSubmit(data: z.infer<typeof FormSchema>) {
    router.push(`/search/${data.type}/${data.query}`);
  }

  return (
    <div className="flex h-full w-full items-center justify-center">
      <div>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="w-full space-y-6 rounded-lg bg-secondary p-8"
          >
            <FormField
              control={form.control}
              name="type"
              render={({ field }) => (
                <FormItem className="space-y-3">
                  <FormLabel>Searching by...</FormLabel>
                  <FormControl>
                    <RadioGroup
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                      className="flex flex-row space-x-4"
                    >
                      <FormItem className="flex items-center space-x-3 space-y-0">
                        <FormControl>
                          <RadioGroupItem value="course" />
                        </FormControl>
                        <FormLabel className="font-normal">Course</FormLabel>
                      </FormItem>
                      <FormItem className="flex items-center space-x-3 space-y-0">
                        <FormControl>
                          <RadioGroupItem value="category" />
                        </FormControl>
                        <FormLabel className="font-normal">Category</FormLabel>
                      </FormItem>
                      <FormItem className="flex items-center space-x-3 space-y-0">
                        <FormControl>
                          <RadioGroupItem value="teacher" />
                        </FormControl>
                        <FormLabel className="font-normal">Teacher</FormLabel>
                      </FormItem>
                    </RadioGroup>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="query"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Query</FormLabel>
                  <FormControl>
                    <Input placeholder="Python" className="w-full" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button type="submit">Search</Button>
          </form>
        </Form>
      </div>
    </div>
  );
}
