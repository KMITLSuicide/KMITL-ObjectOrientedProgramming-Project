import type { Review } from "~/src/lib/definitions/course";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "~/src/components/ui/card";
import { Star } from "lucide-react";

export function ReviewCard({
  review,
  className,
}: {
  review: Review;
  className?: string;
}) {
  return (
    <Card
      className={`w-full cursor-pointer transition-colors ${className}`}
    >
      <div className="flex h-full w-full flex-col items-start pr-6 space-x-2">
          <CardHeader className="pb-2">
            <CardDescription className="flex flex-row justify-center">
              <p>
                {review.user_name}
              </p>
              {review.star > 0 && (
                <span className="text-yellow-400 flex flex-row ml-2 mt-[2px]">
                  {Array(review.star).fill(<Star size={16} />)}
                </span>
              )}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <CardTitle className="ml-2 text-lg">&quot;{review.comment}&quot;</CardTitle>
          </CardContent>
      </div>
    </Card>
  );
}
