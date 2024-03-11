import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "~/src/components/ui/button";
import { Checkbox } from "~/src/components/ui/checkbox";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "~/src/components/ui/form";
import { toast } from "~/src/components/ui/use-toast";
import { completeQuiz } from "~/src/lib/data/course-learn";
import type { CourseLearnMaterialQuiz } from "~/src/lib/definitions/course";


const FormSchema = z.object({
  ids: z.array(z.string()).refine((value) => value.some((item) => item), {
    message: "You have to select at least one item.",
  }),
});



export function CourseLearnQuiz({
  courseID,
  quizData
} : {
  courseID: string,
  quizData: CourseLearnMaterialQuiz
}) {
  const router = useRouter();
  async function sendData(courseID: string, quizID: string, data: { "ids": string[] }) {
    const response = await completeQuiz(courseID, quizID, data);
    if (response?.result === true) {
      toast({
        title: "Success",
        description: "Quiz completed!",
        variant: "default",
      });
      router.push(`/course/${courseID}/learn?fetchProgress=true`);
    } else {
      toast({
        title: "Failed",
        description: `Quiz not completed: ${response?.message}`,
        variant: "destructive",
      });
    }
  }

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
  });

  function onSubmit(data: z.infer<typeof FormSchema>) {
    // toast({
    //   title: "*NOT IMPLEMENTED* Submitted:",
    //   description: (
    //     <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
    //       <code className="text-white">{JSON.stringify(data, null, 2)}</code>
    //     </pre>
    //   ),
    // });

    void sendData(courseID, quizData.id, data);
  }
  return (
    <>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
          <FormField
            control={form.control}
            name="ids"
            render={() => (
              <FormItem>
                <div className="mb-4">
                  <FormLabel className="text-3xl font-bold">
                    {quizData?.name}
                  </FormLabel>
                  <FormDescription>{quizData?.description}</FormDescription>
                </div>
                {quizData?.questions.map((item) => (
                  <FormField
                    key={item.id}
                    control={form.control}
                    name="ids"
                    render={({ field }) => {
                      return (
                        <FormItem
                          key={item.id}
                          className="flex flex-row items-start space-x-3 space-y-0"
                        >
                          <FormControl>
                          <Checkbox
                            checked={field.value?.includes(item.id)}
                            onCheckedChange={(checked) => {
                              const fieldValue = field.value || []; // provide a default value
                              return checked
                                ? field.onChange([...fieldValue, item.id])
                                : field.onChange(
                                    fieldValue.filter(
                                      (value) => value !== item.id,
                                    ),
                                  );
                            }}
                          />
                          </FormControl>
                          <FormLabel className="font-normal">
                            {item.question}
                          </FormLabel>
                        </FormItem>
                      );
                    }}
                  />
                ))}
                <FormMessage />
              </FormItem>
            )}
          />
          <Button type="submit">Submit</Button>
        </form>
      </Form>
    </>
  );
}