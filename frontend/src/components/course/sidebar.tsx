import { cn } from "~/src/lib/utils";
import { Button } from "~/src/components/ui/button";
import { ScrollArea } from "~/src/components/ui/scroll-area";
import Link from "next/link";
import { Checkbox } from "~/src/components/ui/checkbox";
import { completeVideo } from "~/src/lib/data/course-learn";
import { toast } from "~/src/components/ui/use-toast";

export interface SidebarProps extends React.HTMLAttributes<HTMLDivElement> {
  sidebarCategories: SidebarCategory[];
}

export interface SidebarCategory {
  name: string;
  sidebarItems: SidebarItem[];
}

export interface SidebarItem {
  id: string;
  name: string;
  link: string;
  progressSavable: boolean;
  learned?: boolean;
  learnedChangable: boolean;
}

async function saveProgress(id: string, complete: boolean) {
  const response = await completeVideo("courseID", {
    id: id,
    is_complete: complete,
  });

  if (response === false) {
    toast({
      title: "Error",
      description: "Failed to save progress",
      variant: "destructive",
    });
  }
}

export default function CourseLearnSidebar({
  className,
  sidebarCategories,
}: SidebarProps) {
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
                {item.progressSavable && (
                  <Checkbox
                    checked={item.learned}
                    disabled={!item.learnedChangable}
                    onCheckedChange={(checked) => {void saveProgress(item.id, Boolean(checked))}}
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
              <div className="space-y-1">{sidebarItems}</div>
            </div>
          );
        })}
      </div>
    </ScrollArea>
  );
}
