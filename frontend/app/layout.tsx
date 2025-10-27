import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Agno Agent UI',
  description: 'Modern chat interface for AgentOS',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  )
}
