import { zodResolver } from "@hookform/resolvers/zod";
import { useForm, useWatch } from "react-hook-form";
import { z } from "zod";
import { v4 as uuidv4 } from "uuid";

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
import { useRouter } from "next/navigation";
import type { CourseLearnMaterialQuizWithKey } from "~/src/lib/definitions/course";
import { useRef } from "react";
import { createQuestion, deleteQuiz, editQuestion } from "~/src/lib/data/course-edit";

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

export function CourseEditQuiz({
  courseID,
  quizData: initQuizData,
}: {
  courseID: string;
  quizData: CourseLearnMaterialQuizWithKey;
}) {
  const router = useRouter();
  const initialFormData = useRef(initQuizData);
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: initQuizData,
  });

  async function onSubmit(data: z.infer<typeof FormSchema>) {
    for (const question of data.questions) {
      const findResult = initialFormData.current.questions.find(
        (initialQuestion) => initialQuestion.id === question.id,
      );
      if (findResult === undefined) {
        const response = createQuestion(courseID, initQuizData.id, {
          question: question.question,
          correct: question.correct,
        });

        if (response === null) {
          console.log("Failed to create question: ", question.question);
          toast({
            title: "Error",
            description: `Failed to create question: ${question.question}`,
            variant: "destructive",
          });
        }
      }

      if (
        findResult !== undefined &&
        (findResult.question !== question.question ||
          findResult.correct !== question.correct)
      ) {
        const response = editQuestion(courseID, initQuizData.id, question.id, {
          question: question.question,
          correct: question.correct,
        });

        if (response === null) {
          console.log("Failed to edit question: ", question.question);
          toast({
            title: "Error",
            description: `Failed to edit question: ${question.question}`,
            variant: "destructive",
          });
        }
      }
    }
    router.push(`/course/${courseID}/edit/quiz/${initQuizData.id}?fetch=true`);
  }

  const watchedFields = useWatch({ control: form.control });

  function onDeleteQuiz() {
    void deleteQuiz(courseID, initQuizData.id).then((response) => {
      if (response === false) {
        toast({
          title: "Error",
          description: "Failed to delete quiz",
          variant: "destructive",
        });
      } else {
        toast({
          title: "Success",
          description: "Quiz deleted",
        });
        router.push(`/course/${courseID}/edit?fetch=true`);
      }
    });
  }

  return (
    <>
      <h2 className="text-3xl font-extrabold">Editing</h2>
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
                  <FormDescription>
                    {watchedFields?.description}
                  </FormDescription>
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
                  <div className="flex h-full flex-row items-center space-x-2 text-sm text-muted-foreground">
                    <Checkbox checked={true} />
                    <p>Correct Answer</p>
                  </div>
                  <div className="flex h-full flex-row items-center space-x-2 text-sm text-muted-foreground">
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
                                form.setValue(
                                  `questions.${index}.correct`,
                                  Boolean(checked),
                                );
                              }}
                            />
                          </FormControl>
                          <FormControl>
                            <Input
                              value={field.value}
                              onChange={field.onChange}
                            />
                          </FormControl>
                        </FormItem>
                      );
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
      <Button
        variant={"link"}
        className="w-fit"
        onClick={() => {
          form.setValue("questions", [
            ...form.getValues("questions"),
            {
              // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-call
              id: uuidv4(),
              question: `New question`,
              correct: false,
            },
          ]);
        }}
      >
        Add question
      </Button>
      <Button
        variant="destructive"
        onClick={onDeleteQuiz}
        className="mt-6 w-fit"
      >
        Delete Quiz
        </Button>
    </>
  );
}
