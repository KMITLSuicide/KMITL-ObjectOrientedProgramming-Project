"use client";
import ReactPlayer from "react-player"
import { type CourseLearnMaterialVideo } from "~/src/lib/definitions/course"
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

export function CourseLearnVideo ({
  videoData: initVideoData
  } : {
  videoData: CourseLearnMaterialVideo
}) {
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      name: initVideoData.name,
      description: initVideoData.description,
      url: initVideoData.url,
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
      <div className="max-h-2/3 flex flex-col space-y-2">
        <h1 className="text-2xl font-bold">Preview</h1>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <ReactPlayer
          url={watchedFields?.url}
          controls={true}
          width="100%"
          height="320px"
        />
        <h2 className="text-2xl font-bold">{watchedFields?.name}</h2>
        <p>{watchedFields?.description}</p>
      </div>
      <div>
        <hr className="my-4 h-px border-0 bg-muted-foreground" />
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