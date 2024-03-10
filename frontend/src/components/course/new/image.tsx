"use client";

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
import { createMaterialImage } from "~/src/lib/data/course-create";
import { useRouter } from "next/navigation";

const FormSchema = z.object({
  name: z.string().min(1),
  description: z.string().min(1),
  url: z.string().url(),
});

export function CourseCreateImage(
  { courseID }: { courseID: string },
) {
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
  });
  const router = useRouter();

  const watchedFields = useWatch({ control: form.control });

  function onSubmit(data: z.infer<typeof FormSchema>) {
    async function callAPI(data: z.infer<typeof FormSchema>) {
      const image_id = await createMaterialImage(data, courseID);
      if (image_id === null) {
        toast({
          title: "Error",
          description: "Failed to create image material",
          variant: "destructive",
        });
      } else {
        router.push(`/course/${courseID}/edit/image/${image_id}?fetch=true`)
      }
    }
    void callAPI(data);
  }

  return (
    <>
      <h1 className="text-3xl font-bold">Create new image material</h1>
      <div className="max-h-2/3 flex flex-col space-y-2">
        <h2 className="text-2xl font-bold">Preview</h2>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={watchedFields?.url ?? "/notexture.png"}
          alt={watchedFields?.description ?? "description not found"}
          height={320}
          style={{
            objectFit: "contain",
            width: "100%",
            height: "320px",
          }}
        />
        <h2 className="text-2xl font-bold">{watchedFields?.name}</h2>
        <p>{watchedFields?.description}</p>
      </div>
      <div>
        <hr className="my-4 h-px border-0 bg-muted-foreground" />
      </div>
      <div className="h-fit space-y-2">
        <h2 className="text-2xl font-bold">Edit</h2>
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
