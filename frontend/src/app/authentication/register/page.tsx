"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

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
import { RadioGroup, RadioGroupItem } from "~/src/components/ui/radio-group";
import { register } from "~/src/lib/data/authentication";

const FormSchema = z.object({
  type: z.union([z.literal("user"), z.literal("teacher")]),
  name: z.string().min(5, {
    message: "Your name must be at least 5 character",
  }),
  email: z.string().email({
    message: "Invalid email.",
  }),
  password: z.string().min(8, {
    message: "Password must be at least 8 character",
  }),
});

export default function Register() {
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      type: "user",
      name: "",
      email: "",
      password: "",
    },
  });

  async function onSubmit(data: z.infer<typeof FormSchema>) {
    console.log(data);
    const registerStatus = await register(data);

    if (registerStatus) {
      toast({
        title: "Register success",
        description: "You have successfully registered",
      });
      window.location.href = "/";
    } else {
      toast({
        title: "Register failed",
        description: "Please check your account details and try again",
        variant: "destructive",
      });
    }
  }

  return (
    <div className="flex h-full w-full items-center justify-center">
      <div className="h-fit w-fit space-y-4 rounded-lg bg-secondary p-8">
        <h1 className="text-2xl font-extrabold">Register</h1>

        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="w-2/3 space-y-6"
          >
            <FormField
              control={form.control}
              name="type"
              render={({ field }) => (
                <FormItem className="space-y-3">
                  <FormLabel>Are you a...</FormLabel>
                  <FormControl>
                    <RadioGroup
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                      className="flex flex-row space-x-4"
                    >
                      <FormItem className="flex items-center space-x-3 space-y-0">
                        <FormControl>
                          <RadioGroupItem value="user" />
                        </FormControl>
                        <FormLabel className="font-normal">Learner</FormLabel>
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
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Name</FormLabel>
                  <FormControl className="w-72">
                    <Input type="text" {...field}></Input>
                  </FormControl>
                  <FormMessage className="font-semibold" />
                </FormItem>
              )}
            />

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
            <Button type="submit">Register</Button>
            <Button variant="link" asChild>
              <Link href="/authentication/login">Log in</Link>
            </Button>
          </form>
        </Form>
      </div>
    </div>
  );
}
