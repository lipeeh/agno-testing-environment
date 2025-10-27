import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Agno Agent UI',
  description: 'Minimal playground UI for Agno AgentOS',
}

export default function RootLayout({children}:{children:React.ReactNode}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
