import { zodResolver } from "@hookform/resolvers/zod";
import { useForm, useWatch } from "react-hook-form";
import { z } from "zod";
import { v4 as uuidv4 } from 'uuid';

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
import { Input } from "~/src/components/ui/input";
import { toast } from "~/src/components/ui/use-toast";
import { createMaterialQuiz } from "~/src/lib/data/course-create";
import { useRouter } from "next/navigation";

const CourseLearnMaterialQuizQuestionsWithKey = z.object({
  id: z.string(),
  question: z.string(),
  correct: z.boolean(),
});

const FormSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
  description: z.string().min(1),
  questions: z.array(CourseLearnMaterialQuizQuestionsWithKey),
});


export function CourseCreateQuiz(
  { courseID } : { courseID: string },
) {
  const router = useRouter();
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      id: '',
      name: 'Quiz Name',
      description: 'Quiz Description',
      questions: [
            {
              // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-call
              id: uuidv4(),
              question: 'Question 1',
              correct: false,
            },
            {
              // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-call
              id: uuidv4(),
              question: 'Question 2',
              correct: false,
            },
          ],
        }
    })

  async function onSubmit(data: z.infer<typeof FormSchema>) {
    if (!data.questions.some((question) => question.correct)) {
      toast({
        title: "Error",
        description: "At least one question must be correct",
        variant: "destructive",
      });
      return;
    }
    const response = await createMaterialQuiz(data, courseID);
    if (response === null) {
      toast({
        title: "Error",
        description: "Failed to create quiz material",
        variant: "destructive",
      });
    } else {
      toast({
        title: "Success",
        description: "Quiz material created",
        variant: "default",
      });
      router.push(`/course/${courseID}/edit/quiz/${response}?fetch=true`);
    }
  }

  const watchedFields = useWatch({ control: form.control });

  return (
    <>
      <h2 className="text-3xl font-extrabold">New quiz material</h2>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
          <FormField
            control={form.control}
            name="questions"
            render={() => (
              <FormItem>
                <div className="mb-4">
                  <FormLabel className="text-2xl font-bold">
                    {watchedFields?.name}
                  </FormLabel>
                  <FormDescription>{watchedFields?.description}</FormDescription>
                </div>
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

              <div>
                <div className="flex flex-row h-full items-center space-x-2 text-muted-foreground text-sm">
                  <Checkbox checked={true} />
                  <p>Correct Answer</p>
                </div>
                <div className="flex flex-row h-full items-center space-x-2 text-muted-foreground text-sm">
                  <Checkbox checked={false} />
                  <p>Wrong Answer</p>
                </div>
              </div>

                {watchedFields?.questions?.map((question, index) => (
                  <FormField
                    key={question.id}
                    control={form.control}
                    name={`questions.${index}.question`}
                    render={({ field }) => {
                      return (
                        <FormItem
                          key={question.id}
                          className="flex flex-row items-center space-x-2"
                        >
                          <FormControl>
                            <Checkbox
                              checked={question.correct}
                              onCheckedChange={(checked) => {
                                form.setValue(`questions.${index}.correct`, Boolean(checked));
                              }}
                            />
                          </FormControl>
                          <FormControl>
                            <Input value={field.value} onChange={field.onChange} />
                          </FormControl>
                        </FormItem>
                      )
                    }}
                  />
                ))}
                <FormMessage />
              </FormItem>
            )}
          />
          <Button type="submit">Save</Button>
        </form>
      </Form>
      <Button variant={"link"} className="w-fit" onClick={
        () => {
          form.setValue('questions', [
            ...form.getValues('questions'),
            {
              // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-call
              id: uuidv4(),
              question: `New question`,
              correct: false,
            }
          ]);
        }
      }>Add question</Button>
    </>
  );
}