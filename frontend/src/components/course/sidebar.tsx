import { cn } from "~/src/lib/utils";
import { Button } from "~/src/components/ui/button";
import { ScrollArea } from "~/src/components/ui/scroll-area";
import Link from "next/link";

export interface SidebarProps extends React.HTMLAttributes<HTMLDivElement> {
  sidebarCategories: SidebarCategory[]
}

export interface SidebarCategory {
  name: string;
  sidebarItems: SidebarItem[]
}

export interface SidebarItem {
  name: string;
  link: string;
}

export default function CourseLearnSidebar({
  className,
  sidebarCategories,
}: SidebarProps) {
  return (
    <div className={cn("pb-12", className)}>
      <div className="space-y-4 py-4">
        {sidebarCategories.map((category, i) => {
          const sidebarItems = category.sidebarItems.map((item, j) => {
            return (
              <Button
                key={10 * i + j}
                variant="ghost"
                className="w-full justify-start"
                asChild
              >
                <Link href={item.link}>{item.name}</Link>
              </Button>
            );
          });
          return (
            <div key={i} className="py-2">
              <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">
                {category.name}
              </h2>
              <div className="space-y-1 px-2">{sidebarItems}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
