"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Input } from "~/src/components/ui/input";
import { toast } from "~/src/components/ui/use-toast";
import { Toaster } from "~/src/components/ui/toaster";
import { Button } from "~/src/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "~/src/components/ui/form";
import Link from "next/link";

const FormSchema = z.object({
  email: z.string().email({
    message: "Invalid email.",
  }),
  password: z.string().min(8, {
    message: "Password must be at least 8 character",
  }),
})

export default function LogIn() {
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  })
  
  function onSubmit(data: z.infer<typeof FormSchema>) {
    toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify(data, null, 2)}</code>
        </pre>
      ),
    })
  }
   
  return(
    <div className="flex items-center justify-center w-full h-full">
      <div className="h-fit w-fit p-8 bg-secondary rounded-lg space-y-4">
        <h1 className="font-extrabold text-2xl">Log in</h1>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="w-2/3 space-y-6">
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl className="w-72">
                    <Input type="email" {...field}></Input>
                  </FormControl>
                  <FormMessage className="font-semibold" />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl className="w-72">
                    <Input type="password" {...field}></Input>
                  </FormControl>
                  <FormMessage className="font-semibold" />
                </FormItem>
              )}
            />
            <Button type="submit">Log in</Button>
            <Button variant='link' asChild>
              <Link href='/account/register'>Register</Link>
            </Button>
          </form>
        </Form>

      </div>
      <Toaster />
    </div>
  )
}