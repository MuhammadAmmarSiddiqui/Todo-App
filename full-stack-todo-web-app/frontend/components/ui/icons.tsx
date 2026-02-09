import { Loader2, Moon, Sun } from "lucide-react";

import { cn } from "@/src/lib/utils";

export interface IconProps extends React.SVGProps<SVGSVGElement> {
  className?: string;
}

export const Icons = {
  spinner: ({ className, ...props }: IconProps) => (
    <Loader2 className={cn("h-4 w-4 animate-spin", className)} {...props} />
  ),
  sun: ({ className, ...props }: IconProps) => (
    <Sun className={cn("h-4 w-4", className)} {...props} />
  ),
  moon: ({ className, ...props }: IconProps) => (
    <Moon className={cn("h-4 w-4", className)} {...props} />
  ),
  logo: ({ className, ...props }: IconProps) => (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={cn("h-4 w-4", className)}
      {...props}
    >
      <rect width="20" height="14" x="2" y="3" rx="2" />
      <path d="M8 21v-8a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v8" />
    </svg>
  ),
};