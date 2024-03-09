"use client";

import Image from "next/image";
import type { CourseLearnMaterialImage } from "~/src/lib/definitions/course";
import { zodResolver } from "@hookform/resolvers/zod";
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
import { Input } from "~/src/components/ui/input";
import { toast } from "~/src/components/ui/use-toast";

const FormSchema = z.object({
  name: z.string().min(1),
  description: z.string().min(1),
  url: z.string().url(),
});

export function CourseLearnImage({
  imageData: initImageData,
}: {
  imageData: CourseLearnMaterialImage;
}) {
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      name: initImageData.name,
      description: initImageData.description,
      url: initImageData.url,
    },
  });

  const watchedFields = useWatch({ control: form.control });

  function onSubmit(data: z.infer<typeof FormSchema>) {
    toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify(data, null, 2)}</code>
        </pre>
      ),
    });
  }

  return (
    <>
      <div className="flex flex-col w-full h-full space-y-2">
        <h1 className="text-2xl font-bold">Preview</h1>
        <div className="h-full w-full">
          <div className="relative h-full w-full">
            <Image
              alt={watchedFields?.description ?? "description not found"}
              src={watchedFields?.url ?? "/notexture.png"}
              fill
              objectFit="contain"
              className="fixed mb-6 rounded-xl"
            />
          </div>
        </div>
        <h2 className="text-2xl font-bold">{watchedFields?.name}</h2>
        <p>{watchedFields?.description}</p>
      </div>
      <div>
        <hr className="h-px border-0 bg-muted-foreground my-4" />
      </div>
      <div className="h-fit space-y-2">
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
                    <FormLabel>Username</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="url"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>URL</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <Button type="submit" className="my-8">
              Save
            </Button>
          </form>
        </Form>
      </div>
    </>
  );
}
