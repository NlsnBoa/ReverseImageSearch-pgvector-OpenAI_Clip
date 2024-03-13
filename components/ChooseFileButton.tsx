'use client'
import * as React from "react"
import { cn } from "@/lib/utils"

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const ChooseFileButton = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, accept, ...props }, ref) => {

  // In your component or page
  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    event.preventDefault();
    const formData = new FormData();
    const file = event.target.files?.[0]; // Add null check for event.target.files
    console.log("File:",file)
    if (file) {
      formData.append('image', file);

      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      console.log(result);
    }
  };



    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-ful text-slate-500 cursor-pointer rounded-md border border-slate-200 bg-white px-3 py-2 text-sm ring-offset-white file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-800 dark:bg-slate-200 dark:ring-offset-slate-950 dark:placeholder:text-slate-400 dark:focus-visible:ring-slate-300",
          className
        )}
        accept={accept}
        onChange={handleUpload}
        ref={ref}
        {...props}
      />
    )
  }
)
ChooseFileButton.displayName = "ChooseFileButton"

export { ChooseFileButton }
