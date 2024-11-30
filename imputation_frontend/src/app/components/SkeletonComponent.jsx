import { Skeleton } from "@/components/ui/skeleton";

export function SkeletonTable() {
  const times = 10;

  return (
    <div className="flex flex-col space-y-3">
      <Skeleton className="h-12 bg-accent/20 w-full rounded-xl" />
      {Array.from({ length: times }).map((_, index) => (
        <Skeleton key={index} className="h-8 w-full rounded-xl" />
      ))}
    </div>
  );
}
