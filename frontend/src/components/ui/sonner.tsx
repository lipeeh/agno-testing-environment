import { Toaster as Sonner } from "sonner"

export type ToasterProps = React.ComponentProps<typeof Sonner>

export function Toaster(props: ToasterProps) {
  return (
    <Sonner
      richColors
      position="top-right"
      toastOptions={{
        className: "bg-background text-foreground border border-border"
      }}
      {...props}
    />
  )
}
