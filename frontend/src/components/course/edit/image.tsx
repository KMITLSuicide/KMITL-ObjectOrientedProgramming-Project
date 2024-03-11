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
import { editMaterialImage } from "~/src/lib/data/course-edit";
import { useRouter } from "next/navigation";

const FormSchema = z.object({
  name: z.string().min(1),
  description: z.string().min(1),
  url: z.string().min(1),
});

export function CourseEditImage({
  courseID,
  imageData: initImageData,
}: {
  courseID: string;
  imageData: CourseLearnMaterialImage;
}) {
  const router = useRouter();
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
    void editMaterialImage(courseID, initImageData.id, data).then((response) => {
      if (response === false) {
        toast({
          title: "Error",
          description: "Failed to update image",
          variant: "destructive",
        });
      } else {
        toast({
          title: "Success",
          description: "Image updated",
        });
        router.push(`/course/${courseID}/edit/image/${initImageData.id}?fetch=true`);
      }
    });
  }

  return (
    <>
      <div className="max-h-2/3 flex flex-col space-y-2">
        <h1 className="text-2xl font-bold">Preview</h1>
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
