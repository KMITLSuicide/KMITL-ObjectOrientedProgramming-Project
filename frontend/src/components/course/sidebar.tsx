import { cn } from "~/src/lib/utils";
import { Button } from "~/src/components/ui/button";
import { ScrollArea } from "~/src/components/ui/scroll-area";
import Link from "next/link";
import { Checkbox } from "~/src/components/ui/checkbox";
import { completeVideo } from "~/src/lib/data/course-learn";
import { toast } from "~/src/components/ui/use-toast";
import { Progress } from "~/src/components/ui/progress";

export interface SidebarProps extends React.HTMLAttributes<HTMLDivElement> {
  sidebarCategories: SidebarCategory[];
  courseID: string;
  setProgressTotal: (progress: number) => void;
}

export interface SidebarCategory {
  name: string;
  sidebarItems: SidebarItem[];
  progressSavable: boolean;
  progressNormalized: number;
  setProgressNormalized: (progress: number) => void;
}

export interface SidebarItem {
  id: string;
  name: string;
  link: string;
  learned?: boolean;
  learnedChangable: boolean;
}

export default function CourseLearnSidebar({
  className,
  sidebarCategories,
  courseID,
  setProgressTotal,
}: SidebarProps) {
  async function saveProgress(id: string, complete: boolean, setProgressFunction: (progress: number) => void) {
    const response = await completeVideo(courseID, {
      id: id,
      is_complete: complete,
    });

    if (response === false) {
      toast({
        title: "Error",
        description: "Failed to save progress",
        variant: "destructive",
      });
    } else {
      setProgressFunction(response);
    }
  }
  return (
    <ScrollArea className={cn("pb-12", className)}>
      <div className="space-y-4 py-4">
        {sidebarCategories.map((category, i) => {
          const sidebarItems = category.sidebarItems.map((item, j) => {
            return (
              <div
                key={10 * i + j}
                className="flex flex-row items-center space-x-2"
              >
                <Button
                  variant="ghost"
                  className="w-full justify-start"
                  asChild
                >
                  <Link href={item.link}>{item.name}</Link>
                </Button>
                {category.progressSavable && (
                  <Checkbox
                    checked={item.learned}
                    disabled={!item.learnedChangable}
                    onCheckedChange={(checked) => {void saveProgress(item.id, Boolean(checked), category.setProgressNormalized)}}
                  />
                )}
              </div>
            );
          });
          return (
            <div key={i} className="py-2">
              <h2 className="mb-2 text-lg font-semibold tracking-tight">
                {category.name}
              </h2>
              {category.progressSavable && (<div className="flex flex-row items-center space-x-2">
                <p className="text-xs">{(category.progressNormalized * 100)}%</p>
                <Progress
                  value={category.progressNormalized * 100}
                  className="h-2"
                />
              </div>)}
              <div className="space-y-1">{sidebarItems}</div>
            </div>
          );
        })}
      </div>
    </ScrollArea>
  );
}
