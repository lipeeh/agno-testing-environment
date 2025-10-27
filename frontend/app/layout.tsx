import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Agno Agent UI - Complete Testing Environment',
  description: 'Modern chat interface for Agno AgentOS with multi-agent support',
}

export default function RootLayout({children}: {children: React.ReactNode}) {
  return (
    <html lang="en" suppressHydrationWarnings>
      <body className="font-sans antialiased">
        {children}
      </body>
    </html>
  )
}
