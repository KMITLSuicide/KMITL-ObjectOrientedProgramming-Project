"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { type z } from "zod";

import { Input } from "~/src/components/ui/input";
import { toast } from "~/src/components/ui/use-toast";
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
import { useRouter } from "next/navigation";
import { LoginSchema, login } from "~/src/lib/data/authentication";

const FormSchema = LoginSchema;

export default function LogIn() {
  const router = useRouter();

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      username: "",
      password: "",
    },
  });

  async function onSubmit(data: z.infer<typeof FormSchema>) {
    const loginStatus = await login(data);

    if (loginStatus) {
      window.location.href = "/";
    } else {
      toast({
        title: "Login failed",
        description: "Please check your credentials and try again",
        variant: "destructive",
      });
    }
  }

  return (
    <div className="flex h-full w-full items-center justify-center">
      <div className="h-fit w-fit space-y-4 rounded-lg bg-secondary p-8">
        <h1 className="text-2xl font-extrabold">Log in</h1>

        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="w-2/3 space-y-6"
          >
            <FormField
              control={form.control}
              name="username"
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
            <Button variant="link" asChild>
              <Link href="/authentication/register">Register</Link>
            </Button>
          </form>
        </Form>
      </div>
    </div>
  );
}
